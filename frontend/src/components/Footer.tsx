import { Link } from "react-router-dom";
import { Hand, Heart } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-muted border-t border-border mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center">
                <Hand className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gradient">ISHARA</span>
            </div>
            <p className="text-muted-foreground max-w-md">
              Bridging communication through Indian Sign Language. 
              Empowering the deaf and mute community with technology and awareness.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Quick Links</h3>
            <div className="flex flex-col gap-2">
              <Link to="/" className="text-muted-foreground hover:text-primary transition-smooth">
                Home
              </Link>
              <Link to="/learn" className="text-muted-foreground hover:text-primary transition-smooth">
                Learn ISL
              </Link>
              <Link to="/translate" className="text-muted-foreground hover:text-primary transition-smooth">
                AR Translate
              </Link>
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Resources</h3>
            <div className="flex flex-col gap-2">
              <a href="#" className="text-muted-foreground hover:text-primary transition-smooth">
                About ISL
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-smooth">
                Community
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary transition-smooth">
                Support
              </a>
            </div>
          </div>
        </div>
        
        <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-muted-foreground text-sm">
            © 2024 ISHARA. All rights reserved.
          </p>
          <p className="text-muted-foreground text-sm flex items-center gap-2">
            Made with <Heart className="w-4 h-4 text-accent fill-accent" /> for an inclusive India
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
