import { Button } from "./ui/button";
import { ArrowRight, Heart } from "lucide-react";
import { Link } from "react-router-dom";

const CTA = () => {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="relative overflow-hidden rounded-3xl gradient-hero p-12 md:p-16 shadow-medium">
          <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
          
          <div className="relative z-10 max-w-4xl mx-auto text-center text-white">
            <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
              <Heart className="w-5 h-5 fill-white" />
              <span className="font-medium">Join the Movement</span>
            </div>
            
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Be Part of an Inclusive India
            </h2>
            
            <p className="text-xl md:text-2xl mb-8 opacity-90 leading-relaxed max-w-3xl mx-auto">
              Whether you're learning ISL, supporting the deaf community, or simply spreading 
              awareness — every action creates a more connected, inclusive society.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/learn">
                <Button 
                  size="lg" 
                  className="bg-white text-primary hover:bg-white/90 shadow-medium transition-smooth group"
                >
                  Start Your Journey
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-smooth" />
                </Button>
              </Link>
              
              <Link to="/translate">
                <Button 
                  size="lg" 
                  variant="outline" 
                  className="border-2 border-white text-white hover:bg-white/10 backdrop-blur-sm transition-smooth"
                >
                  Explore AR Features
                </Button>
              </Link>
            </div>

            <div className="mt-12 pt-8 border-t border-white/20">
              <p className="text-lg opacity-75">
                Together, we can create a world where everyone is heard and understood.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
