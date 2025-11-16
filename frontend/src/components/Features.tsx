import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { ArrowRight, Video, Smartphone } from "lucide-react";
import { Link } from "react-router-dom";
import learnFeature from "@/assets/learn-feature.jpg";
import arFeature from "@/assets/ar-feature.jpg";

const Features = () => {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16 animate-fade-in-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Experience ISHARA's
            <span className="text-gradient block mt-2">Powerful Features</span>
          </h2>
          <p className="text-xl text-muted-foreground">
            We combine technology and education to create an accessible learning experience 
            for everyone interested in Indian Sign Language.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start">
          {/* Learn ISL Feature */}
          <Card className="overflow-hidden shadow-medium hover:shadow-glow transition-smooth animate-fade-in border-border group">
            <div className="relative overflow-hidden">
              <img 
                src={learnFeature} 
                alt="Learn ISL through videos" 
                className="w-full h-64 object-cover group-hover:scale-105 transition-smooth"
              />
              <div className="absolute top-4 left-4 bg-secondary/90 text-white px-4 py-2 rounded-full flex items-center gap-2">
                <Video className="w-4 h-4" />
                <span className="font-medium">Pre-recorded Videos</span>
              </div>
            </div>
            
            <div className="p-8">
              <h3 className="text-3xl font-bold mb-4 text-foreground">
                Learn ISL at Your Own Pace
              </h3>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                Access our comprehensive library of pre-recorded Indian Sign Language videos. 
                Organized by topics and difficulty levels, perfect for learners, students, 
                teachers, and parents.
              </p>
              
              <ul className="space-y-3 mb-6 text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Categorized lessons from basics to advanced</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Learn common phrases, alphabets, and conversations</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Practice at your own speed, anytime, anywhere</span>
                </li>
              </ul>

              <div className="bg-accent-light p-4 rounded-xl mb-6">
                <p className="text-accent-foreground font-medium text-center">
                  "Start from basics, grow with confidence. Every sign is a step toward inclusion."
                </p>
              </div>
              
              <Link to="/learn">
                <Button className="w-full gradient-secondary text-white shadow-medium hover:shadow-glow transition-smooth group">
                  Explore Video Library
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-smooth" />
                </Button>
              </Link>
            </div>
          </Card>

          {/* AR Translation Feature */}
          <Card className="overflow-hidden shadow-medium hover:shadow-glow transition-smooth animate-fade-in border-border group">
            <div className="relative overflow-hidden">
              <img 
                src={arFeature} 
                alt="AR Translation" 
                className="w-full h-64 object-cover group-hover:scale-105 transition-smooth"
              />
              <div className="absolute top-4 left-4 bg-primary/90 text-white px-4 py-2 rounded-full flex items-center gap-2">
                <Smartphone className="w-4 h-4" />
                <span className="font-medium">AR Technology</span>
              </div>
            </div>
            
            <div className="p-8">
              <h3 className="text-3xl font-bold mb-4 text-foreground">
                Real-Time AR Translation
              </h3>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                Our cutting-edge AR-powered model uses your phone's camera to translate 
                sign language gestures into text and speech in real-time. Break down 
                communication barriers instantly.
              </p>
              
              <ul className="space-y-3 mb-6 text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Instant gesture-to-text translation using AI</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Works offline once models are downloaded</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">✓</span>
                  <span>Helps bridge conversations between deaf and hearing individuals</span>
                </li>
              </ul>

              <div className="bg-primary-light/20 p-4 rounded-xl mb-6 border border-primary/20">
                <p className="text-foreground font-medium text-center">
                  Breaking barriers through technology. Real-time translation, real-world impact.
                </p>
              </div>
              
              <Link to="/translate">
                <Button className="w-full gradient-primary text-white shadow-medium hover:shadow-glow transition-smooth group">
                  Try AR Translation
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-smooth" />
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default Features;
