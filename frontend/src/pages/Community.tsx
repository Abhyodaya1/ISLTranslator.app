import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MessageCircle, Video, Award, Calendar, Users, Heart, TrendingUp, Star } from "lucide-react";

const Community = () => {
  const successStories = [
    {
      name: "Priya Sharma",
      role: "Student, Mumbai",
      story: "Learning ISL through ISHARA helped me make my first deaf friend. Now we chat every day!",
      image: "👧"
    },
    {
      name: "Rajesh Kumar",
      role: "Teacher, Delhi",
      story: "ISHARA transformed my classroom. I can now communicate effectively with all my students.",
      image: "👨‍🏫"
    },
    {
      name: "Anjali Verma",
      role: "Parent, Bangalore",
      story: "Finally, I can have meaningful conversations with my daughter. Thank you ISHARA!",
      image: "👩"
    }
  ];

  const upcomingEvents = [
    {
      title: "ISL Basics Workshop",
      date: "March 15, 2025",
      time: "10:00 AM - 12:00 PM",
      type: "Live Webinar",
      spots: "48 seats left"
    },
    {
      title: "Teacher Training Program",
      date: "March 22, 2025",
      time: "2:00 PM - 5:00 PM",
      type: "Certification Course",
      spots: "Limited seats"
    },
    {
      title: "Community Practice Session",
      date: "March 28, 2025",
      time: "6:00 PM - 7:30 PM",
      type: "Live Practice",
      spots: "Open for all"
    }
  ];

  const forumTopics = [
    {
      title: "Tips for practicing family signs with kids?",
      author: "Meera P.",
      replies: 24,
      category: "Parents",
      time: "2 hours ago"
    },
    {
      title: "Creating inclusive classroom environment",
      author: "Arjun T.",
      replies: 18,
      category: "Teachers",
      time: "5 hours ago"
    },
    {
      title: "How to improve sign speed and fluency?",
      author: "Rohan S.",
      replies: 31,
      category: "Students",
      time: "1 day ago"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-secondary/5 to-background">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto mb-12 animate-fade-in">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 rounded-full bg-secondary/10 text-secondary text-sm font-medium">
                Join the Movement
              </span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Community &
              <span className="text-gradient block mt-2">Support</span>
            </h1>
            <p className="text-xl text-muted-foreground">
              Connect, learn, and grow together. Be part of India's most supportive ISL learning community.
            </p>
          </div>

          {/* Community Stats */}
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <Card className="p-6 text-center border-2 border-primary/20 bg-primary/5 animate-fade-in">
              <Users className="w-8 h-8 text-primary mx-auto mb-2" />
              <p className="text-3xl font-bold text-foreground">5,000+</p>
              <p className="text-sm text-muted-foreground">Active Learners</p>
            </Card>

            <Card className="p-6 text-center border-2 border-secondary/20 bg-secondary/5 animate-fade-in" style={{ animationDelay: "100ms" }}>
              <MessageCircle className="w-8 h-8 text-secondary mx-auto mb-2" />
              <p className="text-3xl font-bold text-foreground">12,000+</p>
              <p className="text-sm text-muted-foreground">Forum Discussions</p>
            </Card>

            <Card className="p-6 text-center border-2 border-accent/20 bg-accent/5 animate-fade-in" style={{ animationDelay: "200ms" }}>
              <Video className="w-8 h-8 text-accent mx-auto mb-2" />
              <p className="text-3xl font-bold text-foreground">150+</p>
              <p className="text-sm text-muted-foreground">Live Sessions</p>
            </Card>

            <Card className="p-6 text-center border-2 border-primary-light/20 bg-primary-light/5 animate-fade-in" style={{ animationDelay: "300ms" }}>
              <Award className="w-8 h-8 text-primary-light mx-auto mb-2" />
              <p className="text-3xl font-bold text-foreground">500+</p>
              <p className="text-sm text-muted-foreground">Certified Teachers</p>
            </Card>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              {/* Success Stories */}
              <div>
                <h2 className="text-3xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <Heart className="w-7 h-7 text-primary" />
                  Success Stories
                </h2>
                <div className="space-y-6">
                  {successStories.map((story, index) => (
                    <Card key={index} className="p-6 border-border hover:shadow-medium transition-smooth animate-fade-in" style={{ animationDelay: `${index * 100}ms` }}>
                      <div className="flex gap-4">
                        <div className="text-5xl">{story.image}</div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-foreground mb-1">{story.name}</h3>
                          <p className="text-sm text-muted-foreground mb-3">{story.role}</p>
                          <p className="text-foreground leading-relaxed">"{story.story}"</p>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Forum Highlights */}
              <div>
                <h2 className="text-3xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <MessageCircle className="w-7 h-7 text-secondary" />
                  ISL Q&A Forum
                </h2>
                <Card className="p-6 border-border">
                  <div className="space-y-4">
                    {forumTopics.map((topic, index) => (
                      <Card key={index} className="p-4 border-border hover:shadow-medium transition-smooth cursor-pointer">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <h4 className="font-bold text-foreground mb-1 hover:text-primary transition-smooth">
                              {topic.title}
                            </h4>
                            <div className="flex items-center gap-3 text-sm text-muted-foreground">
                              <span>by {topic.author}</span>
                              <span>•</span>
                              <span className="px-2 py-0.5 rounded-full bg-accent/10 text-accent text-xs">
                                {topic.category}
                              </span>
                              <span>•</span>
                              <span>{topic.time}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2 text-primary">
                            <MessageCircle className="w-4 h-4" />
                            <span className="font-medium">{topic.replies}</span>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                  <Button className="w-full mt-6 gradient-secondary text-white">
                    Join the Discussion
                  </Button>
                </Card>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-8">
              {/* Upcoming Events */}
              <div>
                <h2 className="text-2xl font-bold mb-6 text-foreground flex items-center gap-2">
                  <Calendar className="w-6 h-6 text-accent" />
                  Upcoming Events
                </h2>
                <div className="space-y-4">
                  {upcomingEvents.map((event, index) => (
                    <Card key={index} className="p-4 border-2 border-accent/20 bg-accent/5 hover:shadow-medium transition-smooth">
                      <div className="flex items-start gap-3 mb-3">
                        <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center text-white font-bold shadow-glow">
                          {event.date.split(' ')[1].slice(0, -1)}
                        </div>
                        <div className="flex-1">
                          <h4 className="font-bold text-foreground mb-1">{event.title}</h4>
                          <p className="text-xs text-muted-foreground">{event.date}</p>
                        </div>
                      </div>
                      <div className="space-y-2 text-sm">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Video className="w-4 h-4" />
                          <span>{event.type}</span>
                        </div>
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Users className="w-4 h-4" />
                          <span>{event.spots}</span>
                        </div>
                      </div>
                      <Button className="w-full mt-4" variant="outline">
                        Register Now
                      </Button>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Teacher Certification */}
              <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-primary/10 to-transparent">
                <Award className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-bold mb-3 text-foreground">Teacher Certification</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Become a certified ISL instructor and make a real difference in inclusive education.
                </p>
                <Button className="w-full gradient-primary text-white shadow-glow">
                  Learn More
                </Button>
              </Card>

              {/* Leaderboard Preview */}
              <Card className="p-6 border-border">
                <h3 className="text-xl font-bold mb-4 text-foreground flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-secondary" />
                  Top Learners
                </h3>
                <div className="space-y-3">
                  {[1, 2, 3].map((rank) => (
                    <div key={rank} className="flex items-center gap-3 p-2 rounded-lg hover:bg-muted/50 transition-smooth">
                      <div className="w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold text-sm">
                        {rank}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-foreground">Learner {rank}</p>
                        <p className="text-xs text-muted-foreground">Level {10 - rank * 2}</p>
                      </div>
                      <Star className="w-4 h-4 text-primary fill-primary" />
                    </div>
                  ))}
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

export default Community;
