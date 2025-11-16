import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Hand } from "lucide-react";

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border shadow-soft">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-glow group-hover:scale-110 transition-bounce">
              <Hand className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-gradient">ISHARA</span>
          </Link>
          
          <div className="hidden md:flex items-center gap-6">
            <Link 
              to="/" 
              className="text-foreground/80 hover:text-primary transition-smooth font-medium"
            >
              Home
            </Link>
            <Link 
              to="/learn" 
              className="text-foreground/80 hover:text-primary transition-smooth font-medium"
            >
              Learn
            </Link>
            <Link 
              to="/dictionary" 
              className="text-foreground/80 hover:text-primary transition-smooth font-medium"
            >
              Dictionary
            </Link>
            <Link 
              to="/ar-practice" 
              className="text-foreground/80 hover:text-primary transition-smooth font-medium"
            >
              AR Practice
            </Link>
            <Link 
              to="/community" 
              className="text-foreground/80 hover:text-primary transition-smooth font-medium"
            >
              Community
            </Link>
            <Link to="/student-dashboard">
              <Button className="gradient-primary text-white shadow-glow hover:shadow-medium transition-smooth">
                My Dashboard
              </Button>
            </Link>
          </div>
          
          <Button 
            variant="ghost" 
            size="icon"
            className="md:hidden"
          >
            <Hand className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
