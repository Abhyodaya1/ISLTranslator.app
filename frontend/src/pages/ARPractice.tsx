import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Camera, CheckCircle, XCircle, Target, Zap, TrendingUp, Award } from "lucide-react";

const ARPractice = () => {
  const practiceModules = [
    {
      title: "Alphabets A-Z",
      difficulty: "Beginner",
      signs: 26,
      accuracy: 92,
      color: "border-primary/50 bg-primary/5"
    },
    {
      title: "Numbers 1-10",
      difficulty: "Beginner",
      signs: 10,
      accuracy: 88,
      color: "border-secondary/50 bg-secondary/5"
    },
    {
      title: "Common Greetings",
      difficulty: "Intermediate",
      signs: 15,
      accuracy: 75,
      color: "border-accent/50 bg-accent/5"
    },
    {
      title: "Daily Conversations",
      difficulty: "Advanced",
      signs: 30,
      accuracy: 0,
      color: "border-primary-light/50 bg-primary-light/5"
    }
  ];

  const feedbackExamples = [
    { type: "correct", message: "Perfect! Your hand position is accurate.", icon: CheckCircle, color: "text-green-500" },
    { type: "tip", message: "Move your hand slightly higher for better clarity.", icon: Target, color: "text-primary" },
    { type: "incorrect", message: "Try bending your fingers more gently.", icon: XCircle, color: "text-destructive" }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-accent/5 to-background">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto mb-12 animate-fade-in">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 rounded-full gradient-primary text-white text-sm font-medium shadow-glow">
                AI-Powered Practice Partner
              </span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Practice with
              <span className="text-gradient block mt-2">Your AR Assistant</span>
            </h1>
            <p className="text-xl text-muted-foreground">
              Get real-time feedback on your signs with our intelligent AR practice system. 
              Perfect your technique confidently from home.
            </p>
          </div>

          {/* Main Practice Section */}
          <div className="grid lg:grid-cols-3 gap-8 mb-12">
            {/* AR Camera View */}
            <Card className="lg:col-span-2 p-8 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-transparent">
              <div className="relative aspect-video bg-gradient-to-br from-muted/50 to-muted rounded-xl border-2 border-border mb-6 flex items-center justify-center">
                <div className="text-center">
                  <Camera className="w-20 h-20 text-primary mx-auto mb-4 animate-pulse" />
                  <p className="text-lg font-bold text-foreground mb-2">Camera View</p>
                  <p className="text-sm text-muted-foreground">Click "Start Practice" to begin</p>
                </div>
                
                {/* AR Overlay Elements */}
                <div className="absolute inset-4 border-2 border-primary/30 rounded-lg pointer-events-none"></div>
                <div className="absolute top-4 left-4 bg-background/90 px-3 py-2 rounded-lg">
                  <p className="text-xs text-muted-foreground">Sign: <span className="font-bold text-foreground">Hello</span></p>
                </div>
              </div>

              <div className="flex gap-4">
                <Button className="flex-1 gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth">
                  <Camera className="w-5 h-5 mr-2" />
                  Start Practice
                </Button>
                <Button variant="outline" className="flex-1">
                  <Target className="w-5 h-5 mr-2" />
                  View Instructions
                </Button>
              </div>
            </Card>

            {/* Live Feedback Panel */}
            <Card className="p-6 border-border">
              <h3 className="text-xl font-bold mb-4 text-foreground flex items-center gap-2">
                <Zap className="w-5 h-5 text-primary" />
                Live Feedback
              </h3>
              
              <div className="space-y-4">
                {feedbackExamples.map((feedback, index) => {
                  const Icon = feedback.icon;
                  return (
                    <div key={index} className={`p-4 rounded-xl border-2 ${
                      feedback.type === 'correct' ? 'border-green-500/30 bg-green-500/5' :
                      feedback.type === 'tip' ? 'border-primary/30 bg-primary/5' :
                      'border-destructive/30 bg-destructive/5'
                    }`}>
                      <div className="flex items-start gap-3">
                        <Icon className={`w-5 h-5 ${feedback.color} flex-shrink-0 mt-0.5`} />
                        <p className="text-sm text-foreground">{feedback.message}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-6 p-4 bg-accent/10 rounded-xl">
                <p className="text-sm font-medium text-center text-accent">
                  Practice more to unlock detailed analysis!
                </p>
              </div>
            </Card>
          </div>

          {/* Practice Modules */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold mb-6 text-foreground flex items-center gap-2">
              <Target className="w-7 h-7 text-primary" />
              Practice Modules
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              {practiceModules.map((module, index) => (
                <Card 
                  key={index}
                  className={`p-6 border-2 ${module.color} hover:shadow-medium transition-smooth cursor-pointer animate-fade-in`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-foreground mb-1">{module.title}</h3>
                      <p className="text-sm text-muted-foreground">{module.signs} signs • {module.difficulty}</p>
                    </div>
                    {module.accuracy > 0 && (
                      <div className="text-right">
                        <p className="text-2xl font-bold text-primary">{module.accuracy}%</p>
                        <p className="text-xs text-muted-foreground">Accuracy</p>
                      </div>
                    )}
                  </div>

                  {module.accuracy > 0 ? (
                    <div className="mb-4">
                      <div className="h-2 bg-muted rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-primary transition-all" 
                          style={{ width: `${module.accuracy}%` }}
                        ></div>
                      </div>
                    </div>
                  ) : (
                    <div className="mb-4 p-3 bg-muted/30 rounded-lg">
                      <p className="text-sm text-muted-foreground text-center">Not started yet</p>
                    </div>
                  )}

                  <Button className="w-full" variant={module.accuracy > 0 ? "default" : "outline"}>
                    {module.accuracy > 0 ? 'Continue Practice' : 'Start Module'}
                  </Button>
                </Card>
              ))}
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Real-Time Analysis</h3>
              <p className="text-sm text-muted-foreground">
                Get instant feedback as you practice each sign with AI-powered recognition
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-6 h-6 text-secondary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Track Progress</h3>
              <p className="text-sm text-muted-foreground">
                Monitor your improvement with detailed accuracy scores and statistics
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mx-auto mb-4">
                <Award className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Earn Achievements</h3>
              <p className="text-sm text-muted-foreground">
                Unlock badges and rewards as you master different sign categories
              </p>
            </Card>
          </div>

          {/* Tips Section */}
          <Card className="p-8 border-2 border-accent/30 bg-gradient-to-br from-accent/10 to-transparent text-center">
            <h2 className="text-3xl font-bold mb-6 text-foreground">
              Pro Tips for Better Practice
            </h2>
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div>
                <h4 className="font-bold mb-2 text-foreground">Good Lighting</h4>
                <p className="text-sm text-muted-foreground">Practice in a well-lit room for better hand detection</p>
              </div>
              <div>
                <h4 className="font-bold mb-2 text-foreground">Clear Background</h4>
                <p className="text-sm text-muted-foreground">Use a plain background to help the AI focus on your hands</p>
              </div>
              <div>
                <h4 className="font-bold mb-2 text-foreground">Camera Distance</h4>
                <p className="text-sm text-muted-foreground">Position yourself 2-3 feet from the camera for optimal results</p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ARPractice;
