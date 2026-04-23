import { useState, useEffect } from "react";
import { useNavigate, Link, useSearchParams } from "react-router-dom";
import { Layout } from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import { Brain, Mail, Lock, ArrowLeft, Loader2, User } from "lucide-react";
import { toast } from "sonner";

export default function Auth() {
  const usernameRegex = /^[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?$/;
  const [searchParams] = useSearchParams();
  const [isSignUp, setIsSignUp] = useState(searchParams.get('signup') === 'true');
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { user, signUp, signIn } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Validate inputs
    if (!email || !email.includes('@')) {
      toast.error("Please enter a valid email address");
      setIsLoading(false);
      return;
    }
    
    if (password.length < 6) {
      toast.error("Password must be at least 6 characters");
      setIsLoading(false);
      return;
    }
    
    if (isSignUp && (!username || username.length < 3)) {
      toast.error("Username must be at least 3 characters");
      setIsLoading(false);
      return;
    }

    if (isSignUp && !usernameRegex.test(username)) {
      toast.error("Username can only contain letters, numbers, dot (.) and underscore (_), and cannot start or end with dot/underscore");
      setIsLoading(false);
      return;
    }

    try {
      if (isSignUp) {
        if (!username) {
          toast.error("Username is required for sign up");
          setIsLoading(false);
          return;
        }
        const { error } = await signUp(email, username, password);
        if (error) {
          toast.error(error.message);
        } else {
          toast.success("User registered successfully. Please log in.");
          setIsSignUp(false);
          setUsername("");
          setPassword("");
          navigate("/auth");
        }
      } else {
        const { error } = await signIn(email, password);
        if (error) {
          toast.error(error.message);
        } else {
          toast.success("Welcome back!");
          navigate("/");
        }
      }
    } catch (error) {
      toast.error("An unexpected error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="relative min-h-[calc(100vh-200px)] flex items-center justify-center py-12 px-4 overflow-hidden">
        <div className="absolute inset-0 gradient-hero -z-10" />
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-primary/10 rounded-full blur-3xl -z-10" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl -z-10" />

        <Card className="w-full max-w-md animate-fade-up border-border/50 shadow-elegant">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl gradient-primary">
              <Brain className="h-7 w-7 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="font-display text-2xl">
                {isSignUp ? "Create an account" : "Welcome back"}
              </CardTitle>
              <CardDescription className="mt-2">
                {isSignUp
                  ? "Sign up to save your recommendations and track progress"
                  : "Sign in to access your personalized dashboard"}
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              {isSignUp && (
                <div className="space-y-2">
                  <Label htmlFor="username">Username</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="username"
                      type="text"
                      placeholder="johndoe"
                      value={username}
                      onChange={(e) => setUsername(e.target.value.replace(/[^A-Za-z0-9._]/g, ""))}
                      className="pl-10"
                      minLength={3}
                      pattern="[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?"
                      title="Use letters/numbers with optional dot or underscore in the middle only (not at start or end)"
                      required
                    />
                  </div>
                </div>
              )}
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>
              <Button
                type="submit"
                variant="hero"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {isSignUp ? "Creating account..." : "Signing in..."}
                  </>
                ) : (
                  <>{isSignUp ? "Create Account" : "Sign In"}</>
                )}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-muted-foreground">
                {isSignUp ? "Already have an account? " : "Don't have an account? "}
              </span>
              <button
                type="button"
                onClick={() => setIsSignUp(!isSignUp)}
                className="text-primary hover:underline font-medium"
              >
                {isSignUp ? "Sign in" : "Sign up"}
              </button>
            </div>

            <div className="mt-4 text-center">
              <Link
                to="/"
                className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to home
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
