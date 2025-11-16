import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, BookOpen, Users, Clock } from "lucide-react";
import learnFeature from "@/assets/learn-feature.jpg";

const Learn = () => {
  const categories = [
    {
      title: "Basics & Alphabets",
      description: "Start your journey with ISL alphabets and numbers",
      videos: 45,
      duration: "3-5 min each",
      color: "border-primary/50 bg-primary/5"
    },
    {
      title: "Common Phrases",
      description: "Essential everyday conversations and greetings",
      videos: 60,
      duration: "5-8 min each",
      color: "border-secondary/50 bg-secondary/5"
    },
    {
      title: "Family & Relationships",
      description: "Signs for family members and social connections",
      videos: 35,
      duration: "4-6 min each",
      color: "border-accent/50 bg-accent/5"
    },
    {
      title: "Education & Learning",
      description: "Academic terms and classroom communication",
      videos: 50,
      duration: "6-10 min each",
      color: "border-primary-light/50 bg-primary-light/5"
    },
    {
      title: "Daily Activities",
      description: "Signs for routine tasks and activities",
      videos: 55,
      duration: "4-7 min each",
      color: "border-secondary-light/50 bg-secondary-light/5"
    },
    {
      title: "Emotions & Feelings",
      description: "Express emotions and understand feelings",
      videos: 40,
      duration: "3-5 min each",
      color: "border-accent-light/50 bg-accent-light/5"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-32 pb-16 bg-gradient-to-b from-muted/50 to-background">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6 animate-fade-in">
              <div className="inline-block">
                <span className="px-4 py-2 rounded-full bg-secondary/10 text-secondary text-sm font-medium">
                  Video Learning Platform
                </span>
              </div>
              
              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                Learn Indian Sign Language
                <span className="text-gradient block mt-2">At Your Own Pace</span>
              </h1>
              
              <p className="text-xl text-muted-foreground leading-relaxed">
                Our comprehensive video library makes learning ISL accessible and enjoyable 
                for everyone. Start from basics and progress to advanced conversations.
              </p>

              <div className="bg-accent-light p-6 rounded-xl border border-accent/20">
                <p className="text-accent-foreground font-medium text-lg">
                  "Every sign you learn is a bridge to understanding. Start your journey today 
                  and become part of a more inclusive society."
                </p>
              </div>
            </div>
            
            <div className="relative animate-scale-in">
              <img 
                src={learnFeature} 
                alt="Learn ISL" 
                className="w-full rounded-2xl shadow-medium"
              />
              <div className="absolute inset-0 bg-gradient-primary/20 rounded-2xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-card border-y border-border">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div className="p-4">
              <Play className="w-8 h-8 text-primary mx-auto mb-2" />
              <h3 className="text-3xl font-bold text-foreground">285+</h3>
              <p className="text-muted-foreground">Video Lessons</p>
            </div>
            <div className="p-4">
              <BookOpen className="w-8 h-8 text-secondary mx-auto mb-2" />
              <h3 className="text-3xl font-bold text-foreground">6</h3>
              <p className="text-muted-foreground">Categories</p>
            </div>
            <div className="p-4">
              <Users className="w-8 h-8 text-accent mx-auto mb-2" />
              <h3 className="text-3xl font-bold text-foreground">5000+</h3>
              <p className="text-muted-foreground">Active Learners</p>
            </div>
            <div className="p-4">
              <Clock className="w-8 h-8 text-primary-light mx-auto mb-2" />
              <h3 className="text-3xl font-bold text-foreground">3-10</h3>
              <p className="text-muted-foreground">Minutes per Video</p>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Choose Your Learning Path
            </h2>
            <p className="text-xl text-muted-foreground">
              Browse our organized video categories and start learning ISL step by step
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category, index) => (
              <Card 
                key={index}
                className={`p-6 border-2 ${category.color} hover:shadow-medium transition-smooth animate-fade-in group cursor-pointer`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex items-start justify-between mb-4">
                  <Play className="w-10 h-10 text-primary group-hover:scale-110 transition-bounce" />
                  <span className="text-sm font-medium text-muted-foreground">
                    {category.videos} videos
                  </span>
                </div>
                
                <h3 className="text-2xl font-bold mb-2 text-foreground group-hover:text-primary transition-smooth">
                  {category.title}
                </h3>
                <p className="text-muted-foreground mb-4">
                  {category.description}
                </p>
                
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock className="w-4 h-4" />
                  <span>{category.duration}</span>
                </div>
                
                <Button 
                  className="w-full mt-6 bg-background hover:bg-muted border border-border group-hover:border-primary transition-smooth"
                  variant="outline"
                >
                  Browse Videos
                </Button>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-12">
              Why Learn with <span className="text-gradient">ISHARA</span>?
            </h2>
            
            <div className="grid md:grid-cols-2 gap-8">
              <Card className="p-6 bg-card border-border">
                <h3 className="text-xl font-bold mb-3 text-foreground">For Students & Learners</h3>
                <p className="text-muted-foreground">
                  Build communication skills that open doors to friendship, understanding, 
                  and opportunities with the deaf community.
                </p>
              </Card>
              
              <Card className="p-6 bg-card border-border">
                <h3 className="text-xl font-bold mb-3 text-foreground">For Teachers & Educators</h3>
                <p className="text-muted-foreground">
                  Access teaching resources to create inclusive classrooms and support 
                  deaf students effectively.
                </p>
              </Card>
              
              <Card className="p-6 bg-card border-border">
                <h3 className="text-xl font-bold mb-3 text-foreground">For Parents & Families</h3>
                <p className="text-muted-foreground">
                  Connect deeply with deaf family members through their primary language 
                  and strengthen family bonds.
                </p>
              </Card>
              
              <Card className="p-6 bg-card border-border">
                <h3 className="text-xl font-bold mb-3 text-foreground">For Everyone</h3>
                <p className="text-muted-foreground">
                  Be part of a movement towards a more inclusive India where everyone 
                  can communicate freely.
                </p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Learn;
