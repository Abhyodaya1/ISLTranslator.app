import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, BookOpen, CheckCircle, Clock, Download, PlusCircle, BarChart, FileText } from "lucide-react";
import { Progress } from "@/components/ui/progress";

const TeacherDashboard = () => {
  const students = [
    { name: "Priya Sharma", progress: 85, lessons: 42, lastActive: "Today" },
    { name: "Arjun Patel", progress: 72, lessons: 38, lastActive: "Yesterday" },
    { name: "Meera Singh", progress: 91, lessons: 48, lastActive: "Today" },
    { name: "Rohan Kumar", progress: 65, lessons: 32, lastActive: "2 days ago" },
  ];

  const lessonPlans = [
    { title: "ISL Alphabets A-Z", lessons: 26, duration: "2 weeks", status: "Active" },
    { title: "Daily Conversations", lessons: 15, duration: "1 week", status: "Active" },
    { title: "Classroom Vocabulary", lessons: 20, duration: "10 days", status: "Draft" },
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-secondary/5 to-background">
        <div className="container mx-auto px-4">
          {/* Welcome Header */}
          <div className="mb-12 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Welcome, <span className="text-gradient">Teacher</span>!
            </h1>
            <p className="text-xl text-muted-foreground">
              Creating inclusive classrooms, one sign at a time.
            </p>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <Button className="h-auto p-6 flex-col gradient-primary text-white shadow-medium hover:shadow-glow transition-smooth">
              <PlusCircle className="w-8 h-8 mb-2" />
              <span className="text-lg font-bold">New Lesson Plan</span>
            </Button>
            
            <Button className="h-auto p-6 flex-col gradient-secondary text-white shadow-medium hover:shadow-glow transition-smooth">
              <Users className="w-8 h-8 mb-2" />
              <span className="text-lg font-bold">Add Student</span>
            </Button>
            
            <Button className="h-auto p-6 flex-col gradient-accent text-white shadow-medium hover:shadow-glow transition-smooth">
              <FileText className="w-8 h-8 mb-2" />
              <span className="text-lg font-bold">Assign Quiz</span>
            </Button>
            
            <Button className="h-auto p-6 flex-col bg-muted hover:bg-muted/80 text-foreground border-2 border-border transition-smooth">
              <Download className="w-8 h-8 mb-2" />
              <span className="text-lg font-bold">Resources</span>
            </Button>
          </div>

          {/* Stats Overview */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <Card className="p-6 border-2 border-primary/20 bg-primary/5">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center">
                  <Users className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">24</p>
                  <p className="text-sm text-muted-foreground">Total Students</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-secondary/20 bg-secondary/5">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-secondary/20 flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-secondary" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">12</p>
                  <p className="text-sm text-muted-foreground">Active Lessons</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-accent/20 bg-accent/5">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">81%</p>
                  <p className="text-sm text-muted-foreground">Avg Completion</p>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-2 border-primary-light/20 bg-primary-light/5">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary-light/20 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-primary-light" />
                </div>
                <div>
                  <p className="text-3xl font-bold text-foreground">186</p>
                  <p className="text-sm text-muted-foreground">Hours Taught</p>
                </div>
              </div>
            </Card>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Student Progress */}
            <div className="lg:col-span-2 space-y-6">
              <Card className="p-6 border-border">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
                    <Users className="w-6 h-6 text-primary" />
                    Student Progress
                  </h2>
                  <Button variant="outline">View All</Button>
                </div>

                <div className="space-y-4">
                  {students.map((student, index) => (
                    <Card key={index} className="p-4 border-border hover:shadow-medium transition-smooth">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold">
                            {student.name.charAt(0)}
                          </div>
                          <div>
                            <h3 className="font-bold text-foreground">{student.name}</h3>
                            <p className="text-sm text-muted-foreground">
                              {student.lessons} lessons • Last active {student.lastActive}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold text-primary">{student.progress}%</p>
                        </div>
                      </div>
                      <Progress value={student.progress} className="h-2" />
                    </Card>
                  ))}
                </div>
              </Card>

              {/* Class Analytics */}
              <Card className="p-6 border-border">
                <h2 className="text-2xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <BarChart className="w-6 h-6 text-secondary" />
                  Class Performance
                </h2>
                <div className="h-64 flex items-center justify-center bg-muted/20 rounded-xl">
                  <p className="text-muted-foreground">Performance chart visualization</p>
                </div>
              </Card>
            </div>

            {/* Lesson Plans */}
            <div className="space-y-6">
              <Card className="p-6 border-border">
                <h2 className="text-2xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <BookOpen className="w-6 h-6 text-accent" />
                  Lesson Plans
                </h2>
                
                <div className="space-y-4">
                  {lessonPlans.map((plan, index) => (
                    <Card key={index} className="p-4 border-border hover:shadow-medium transition-smooth cursor-pointer">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-bold text-foreground">{plan.title}</h4>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          plan.status === 'Active' 
                            ? 'bg-primary/10 text-primary' 
                            : 'bg-muted text-muted-foreground'
                        }`}>
                          {plan.status}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {plan.lessons} lessons • {plan.duration}
                      </p>
                    </Card>
                  ))}
                </div>

                <Button className="w-full mt-4" variant="outline">
                  <PlusCircle className="w-4 h-4 mr-2" />
                  Create New Plan
                </Button>
              </Card>

              {/* Classroom Tools */}
              <Card className="p-6 border-2 border-accent/30 bg-gradient-to-br from-accent/10 to-transparent">
                <h3 className="text-xl font-bold mb-4 text-foreground">Classroom Mode</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Project lessons on screen for whole-class learning with large, clear visuals.
                </p>
                <Button className="w-full gradient-accent text-white">
                  Launch Projector View
                </Button>
              </Card>

              {/* Downloads */}
              <Card className="p-6 border-border">
                <h3 className="text-xl font-bold mb-4 text-foreground flex items-center gap-2">
                  <Download className="w-5 h-5 text-primary" />
                  Resources
                </h3>
                <div className="space-y-3">
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="w-4 h-4 mr-2" />
                    Practice Worksheets
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="w-4 h-4 mr-2" />
                    Assessment PDFs
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="w-4 h-4 mr-2" />
                    Lesson Guides
                  </Button>
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

export default TeacherDashboard;
