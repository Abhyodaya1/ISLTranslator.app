import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Trophy, Flame, Star, BookOpen, Clock, Target, Award, TrendingUp } from "lucide-react";
import { Progress } from "@/components/ui/progress";

const StudentDashboard = () => {
  const achievements = [
    { icon: Star, title: "First Steps", description: "Completed 10 lessons", unlocked: true },
    { icon: Trophy, title: "Week Warrior", description: "7-day learning streak", unlocked: true },
    { icon: Award, title: "Sign Master", description: "Mastered 50 signs", unlocked: false },
    { icon: Target, title: "Perfect Practice", description: "100% accuracy in 5 lessons", unlocked: false },
  ];

  const recentLessons = [
    { title: "Common Greetings", category: "Basics", progress: 100, time: "Yesterday" },
    { title: "Family Members", category: "Relationships", progress: 75, time: "2 days ago" },
    { title: "Daily Activities", category: "Intermediate", progress: 40, time: "3 days ago" },
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-primary/5 to-background">
        <div className="container mx-auto px-4">
          {/* Welcome Header */}
          <div className="mb-12 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Welcome back, <span className="text-gradient">Learner</span>!
            </h1>
            <p className="text-xl text-muted-foreground">
              Keep up the amazing progress! You're building bridges of communication.
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <Card className="p-6 border-2 border-primary/20 bg-primary/5 animate-fade-in">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center">
                  <Flame className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">7</p>
                  <p className="text-sm text-muted-foreground">Day Streak</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-secondary/20 bg-secondary/5 animate-fade-in" style={{ animationDelay: "100ms" }}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-secondary/20 flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-secondary" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">42</p>
                  <p className="text-sm text-muted-foreground">Lessons Done</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-accent/20 bg-accent/5 animate-fade-in" style={{ animationDelay: "200ms" }}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                  <Star className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">850</p>
                  <p className="text-sm text-muted-foreground">Points Earned</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-primary-light/20 bg-primary-light/5 animate-fade-in" style={{ animationDelay: "300ms" }}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary-light/20 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-primary-light" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">12.5</p>
                  <p className="text-sm text-muted-foreground">Hours Learning</p>
                </div>
              </div>
            </Card>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Recent Lessons */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="p-6 border-border">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-foreground">Continue Learning</h2>
                  <Button variant="outline">View All</Button>
                </div>

                <div className="space-y-4">
                  {recentLessons.map((lesson, index) => (
                    <Card key={index} className="p-4 border-border hover:shadow-medium transition-smooth cursor-pointer">
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <h3 className="font-bold text-foreground">{lesson.title}</h3>
                          <p className="text-sm text-muted-foreground">{lesson.category} • {lesson.time}</p>
                        </div>
                        <span className="text-sm font-medium text-primary">{lesson.progress}%</span>
                      </div>
                      <Progress value={lesson.progress} className="h-2" />
                    </Card>
                  ))}
                </div>
              </Card>

              {/* Daily Challenge */}
              <Card className="p-6 border-2 border-accent/30 bg-gradient-to-br from-accent/10 to-transparent">
                <div className="flex items-start gap-4">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-glow">
                    <Target className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold mb-2 text-foreground">Today's Challenge</h3>
                    <p className="text-muted-foreground mb-4">Learn 5 new signs related to emotions and feelings</p>
                    <div className="flex items-center gap-4">
                      <Progress value={60} className="flex-1 h-2" />
                      <span className="text-sm font-medium text-foreground">3/5</span>
                    </div>
                    <Button className="mt-4 gradient-primary text-white">Continue Challenge</Button>
                  </div>
                </div>
              </Card>
            </div>

            {/* Achievements */}
            <div className="space-y-6">
              <Card className="p-6 border-border">
                <h2 className="text-2xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <Trophy className="w-6 h-6 text-primary" />
                  Achievements
                </h2>
                
                <div className="space-y-4">
                  {achievements.map((achievement, index) => {
                    const Icon = achievement.icon;
                    return (
                      <div 
                        key={index}
                        className={`p-4 rounded-xl border-2 transition-smooth ${
                          achievement.unlocked 
                            ? 'border-primary/30 bg-primary/5' 
                            : 'border-border bg-muted/20 opacity-60'
                        }`}
                      >
                        <div className="flex items-center gap-3 mb-2">
                          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                            achievement.unlocked ? 'bg-gradient-primary shadow-glow' : 'bg-muted'
                          }`}>
                            <Icon className={`w-5 h-5 ${achievement.unlocked ? 'text-white' : 'text-muted-foreground'}`} />
                          </div>
                          <div className="flex-1">
                            <h4 className="font-bold text-sm text-foreground">{achievement.title}</h4>
                            <p className="text-xs text-muted-foreground">{achievement.description}</p>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>

              {/* Weekly Progress */}
              <Card className="p-6 border-border">
                <h3 className="text-xl font-bold mb-4 text-foreground flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-secondary" />
                  This Week
                </h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-muted-foreground">Weekly Goal</span>
                      <span className="text-sm font-medium text-foreground">70%</span>
                    </div>
                    <Progress value={70} className="h-2" />
                  </div>
                  <p className="text-sm text-muted-foreground">
                    You've completed 7 out of 10 weekly lessons. Keep going!
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default StudentDashboard;
