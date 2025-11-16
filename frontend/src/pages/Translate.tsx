import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Camera, Zap, Globe, Shield, Smartphone, Users } from "lucide-react";
import arFeature from "@/assets/ar-feature.jpg";

const Translate = () => {
  const features = [
    {
      icon: Camera,
      title: "Real-Time Translation",
      description: "Instantly translate sign language gestures to text using your device camera",
      color: "text-primary"
    },
    {
      icon: Zap,
      title: "AI-Powered Accuracy",
      description: "Advanced machine learning ensures high precision in gesture recognition",
      color: "text-secondary"
    },
    {
      icon: Globe,
      title: "Indian Sign Language",
      description: "Specifically trained on ISL gestures for authentic Indian communication",
      color: "text-accent"
    },
    {
      icon: Shield,
      title: "Privacy First",
      description: "All processing happens on your device - your privacy is protected",
      color: "text-primary-light"
    }
  ];

  const benefits = [
    {
      title: "Education Access",
      description: "Help deaf students participate fully in classrooms and online learning",
      icon: "🎓"
    },
    {
      title: "Healthcare Communication",
      description: "Enable clear communication between patients and healthcare providers",
      icon: "🏥"
    },
    {
      title: "Employment Opportunities",
      description: "Break barriers in workplace communication and job interviews",
      icon: "💼"
    },
    {
      title: "Social Inclusion",
      description: "Foster connections and conversations in everyday social situations",
      icon: "🤝"
    },
    {
      title: "Public Services",
      description: "Make government services and public spaces more accessible",
      icon: "🏛️"
    },
    {
      title: "Family Connections",
      description: "Strengthen bonds between deaf and hearing family members",
      icon: "❤️"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-32 pb-16 bg-gradient-to-b from-primary/5 to-background">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6 animate-fade-in">
              <div className="inline-block">
                <span className="px-4 py-2 rounded-full gradient-primary text-white text-sm font-medium shadow-glow">
                  Powered by Advanced AR & AI
                </span>
              </div>
              
              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                Break Communication Barriers
                <span className="text-gradient block mt-2">With AR Translation</span>
              </h1>
              
              <p className="text-xl text-muted-foreground leading-relaxed">
                Experience the future of inclusive communication. Our AR-powered translator 
                uses your camera to convert sign language gestures into text and speech in real-time.
              </p>

              <Button size="lg" className="gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth group">
                <Camera className="mr-2 w-5 h-5" />
                Launch AR Translator
              </Button>
            </div>
            
            <div className="relative animate-scale-in">
              <div className="absolute inset-0 bg-gradient-primary opacity-20 blur-3xl rounded-full"></div>
              <img 
                src={arFeature} 
                alt="AR Translation" 
                className="relative w-full rounded-2xl shadow-medium hover:shadow-glow transition-smooth"
              />
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Simple, fast, and incredibly accurate translation in just three steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="p-8 text-center bg-card border-border shadow-soft hover:shadow-medium transition-smooth">
              <div className="w-16 h-16 rounded-full gradient-primary flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6 shadow-glow">
                1
              </div>
              <Smartphone className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-3 text-foreground">Open the App</h3>
              <p className="text-muted-foreground">
                Launch ISHARA's AR translator on your smartphone or tablet
              </p>
            </Card>

            <Card className="p-8 text-center bg-card border-border shadow-soft hover:shadow-medium transition-smooth">
              <div className="w-16 h-16 rounded-full gradient-secondary flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6 shadow-glow">
                2
              </div>
              <Camera className="w-12 h-12 text-secondary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-3 text-foreground">Point Camera</h3>
              <p className="text-muted-foreground">
                Aim your camera at the person signing in Indian Sign Language
              </p>
            </Card>

            <Card className="p-8 text-center bg-card border-border shadow-soft hover:shadow-medium transition-smooth">
              <div className="w-16 h-16 rounded-full gradient-warm flex items-center justify-center text-white text-2xl font-bold mx-auto mb-6 shadow-glow">
                3
              </div>
              <Zap className="w-12 h-12 text-accent mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-3 text-foreground">Instant Translation</h3>
              <p className="text-muted-foreground">
                See gestures translated to text on screen in real-time
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Powerful Technology,
              <span className="text-gradient block mt-2">Accessible to Everyone</span>
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {features.map((feature, index) => (
              <Card 
                key={index}
                className="p-8 bg-card border-border hover:shadow-medium transition-smooth animate-fade-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <feature.icon className={`w-12 h-12 ${feature.color} mb-4`} />
                <h3 className="text-2xl font-bold mb-3 text-foreground">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Real-World Impact */}
      <section className="py-20 bg-gradient-warm text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Real-World Impact
            </h2>
            <p className="text-xl opacity-90">
              See how AR translation is transforming lives across India
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {benefits.map((benefit, index) => (
              <Card 
                key={index}
                className="p-6 bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 transition-smooth"
              >
                <div className="text-4xl mb-4">{benefit.icon}</div>
                <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                <p className="opacity-90">{benefit.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <Card className="p-12 md:p-16 text-center bg-gradient-to-br from-primary/10 to-secondary/10 border-border shadow-medium">
            <Users className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-foreground">
              Join Thousands Using AR Translation
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
              Be part of the movement creating a truly inclusive India where communication 
              barriers no longer exist.
            </p>
            <Button size="lg" className="gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth">
              <Camera className="mr-2 w-5 h-5" />
              Start Translating Now
            </Button>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Translate;
