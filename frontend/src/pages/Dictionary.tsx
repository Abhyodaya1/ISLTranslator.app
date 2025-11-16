import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, BookOpen, Star, Play, Volume2 } from "lucide-react";
import { useState } from "react";

const Dictionary = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const categories = [
    "Alphabets", "Numbers", "Greetings", "Family", "Colors", 
    "Animals", "Food", "Emotions", "Actions", "Places"
  ];

  const signs = [
    { word: "Hello", category: "Greetings", difficulty: "Basic", isFavorite: true },
    { word: "Thank You", category: "Greetings", difficulty: "Basic", isFavorite: false },
    { word: "Mother", category: "Family", difficulty: "Basic", isFavorite: true },
    { word: "Happy", category: "Emotions", difficulty: "Basic", isFavorite: false },
    { word: "Eat", category: "Actions", difficulty: "Basic", isFavorite: false },
    { word: "School", category: "Places", difficulty: "Basic", isFavorite: true },
  ];

  const filteredSigns = signs.filter(sign => 
    sign.word.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sign.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <section className="pt-32 pb-16 bg-gradient-to-b from-accent/5 to-background">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="text-center max-w-3xl mx-auto mb-12 animate-fade-in">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium">
                Interactive ISL Dictionary
              </span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Search & Learn
              <span className="text-gradient block mt-2">Any Sign, Anytime</span>
            </h1>
            <p className="text-xl text-muted-foreground">
              Explore our comprehensive dictionary of Indian Sign Language with video demonstrations
            </p>
          </div>

          {/* Search Bar */}
          <Card className="p-6 mb-12 border-2 border-primary/20 shadow-medium animate-fade-in">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input 
                type="text"
                placeholder="Search for any word, category, or gesture..."
                className="pl-12 h-14 text-lg border-border"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </Card>

          {/* Categories */}
          <div className="mb-12 animate-fade-in">
            <h2 className="text-2xl font-bold mb-6 text-foreground flex items-center gap-2">
              <BookOpen className="w-6 h-6 text-primary" />
              Browse by Category
            </h2>
            <div className="flex flex-wrap gap-3">
              {categories.map((category, index) => (
                <Button
                  key={index}
                  variant="outline"
                  className="rounded-full hover:bg-primary hover:text-white hover:border-primary transition-smooth"
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>

          {/* Sign Cards Grid */}
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-foreground">
                {searchTerm ? `Results for "${searchTerm}"` : 'Popular Signs'}
              </h2>
              <Button variant="outline">
                <Star className="w-4 h-4 mr-2" />
                View Favorites
              </Button>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredSigns.map((sign, index) => (
                <Card 
                  key={index}
                  className="overflow-hidden border-border hover:shadow-medium transition-smooth cursor-pointer group animate-fade-in"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {/* Video Thumbnail */}
                  <div className="relative bg-gradient-to-br from-primary/10 to-secondary/10 h-48 flex items-center justify-center">
                    <Play className="w-16 h-16 text-primary group-hover:scale-110 transition-smooth" />
                    <div className="absolute top-3 right-3">
                      <Button
                        size="icon"
                        variant="secondary"
                        className="w-8 h-8 rounded-full shadow-soft"
                      >
                        <Star className={`w-4 h-4 ${sign.isFavorite ? 'fill-primary text-primary' : ''}`} />
                      </Button>
                    </div>
                    <div className="absolute bottom-3 left-3">
                      <span className="px-3 py-1 rounded-full bg-background/90 text-xs font-medium">
                        {sign.difficulty}
                      </span>
                    </div>
                  </div>

                  {/* Card Content */}
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="text-xl font-bold text-foreground group-hover:text-primary transition-smooth">
                          {sign.word}
                        </h3>
                        <p className="text-sm text-muted-foreground">{sign.category}</p>
                      </div>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="w-8 h-8"
                      >
                        <Volume2 className="w-4 h-4" />
                      </Button>
                    </div>

                    <div className="flex gap-2 mt-4">
                      <Button className="flex-1 gradient-primary text-white text-sm">
                        Watch Video
                      </Button>
                      <Button variant="outline" className="text-sm">
                        Practice
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Play className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Slow Motion</h3>
              <p className="text-sm text-muted-foreground">
                Watch signs in slow motion to understand every movement clearly
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mx-auto mb-4">
                <Volume2 className="w-6 h-6 text-secondary" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Audio Guide</h3>
              <p className="text-sm text-muted-foreground">
                Listen to pronunciation and detailed explanations for each sign
              </p>
            </Card>

            <Card className="p-6 border-border text-center">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mx-auto mb-4">
                <Star className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-foreground">Save Favorites</h3>
              <p className="text-sm text-muted-foreground">
                Bookmark important signs for quick access and revision
              </p>
            </Card>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Dictionary;
