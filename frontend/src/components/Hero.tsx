import { Button } from "./ui/button";
import { ArrowRight, Play } from "lucide-react";
import { Link } from "react-router-dom";
import heroImage from "@/assets/hero-image.jpg";

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center pt-20 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 gradient-hero opacity-10"></div>
      
      <div className="container mx-auto px-4 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 animate-fade-in">
            <div className="inline-block">
              <span className="px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
                Empowering through Indian Sign Language
              </span>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              Bridging Communication,
              <span className="text-gradient block mt-2">Building Inclusion</span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-xl leading-relaxed">
              ISHARA is dedicated to empowering India's deaf and mute community through 
              innovative technology, education, and awareness of Indian Sign Language.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/learn">
                <Button size="lg" className="gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth group">
                  Start Learning ISL
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-smooth" />
                </Button>
              </Link>
              
              <Link to="/translate">
                <Button 
                  size="lg" 
                  variant="outline" 
                  className="border-2 border-primary text-primary hover:bg-primary/5 transition-smooth group"
                >
                  <Play className="mr-2 w-5 h-5 group-hover:scale-110 transition-smooth" />
                  Try AR Translation
                </Button>
              </Link>
            </div>
          </div>
          
          <div className="relative animate-scale-in">
            <div className="absolute inset-0 bg-gradient-primary opacity-20 blur-3xl rounded-full"></div>
            <img 
              src={heroImage} 
              alt="Hands forming sign language" 
              className="relative w-full h-auto rounded-3xl shadow-medium hover:shadow-glow transition-smooth"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
