import { Card } from "./ui/card";
import { Users, GraduationCap, Heart, TrendingUp } from "lucide-react";

const WhyISL = () => {
  const stats = [
    {
      icon: Users,
      number: "63 Lakh+",
      label: "Deaf individuals in India",
      color: "text-primary"
    },
    {
      icon: GraduationCap,
      number: "98%",
      label: "Lack formal ISL education",
      color: "text-secondary"
    },
    {
      icon: Heart,
      number: "Limited",
      label: "Communication accessibility",
      color: "text-accent"
    },
    {
      icon: TrendingUp,
      number: "Growing",
      label: "Need for ISL awareness",
      color: "text-primary-light"
    }
  ];

  return (
    <section className="py-20 bg-muted/50">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-16 animate-fade-in-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Why Indian Sign Language
            <span className="text-gradient block mt-2">Matters Now</span>
          </h2>
          <p className="text-xl text-muted-foreground leading-relaxed">
            In India, millions of deaf and mute individuals face daily communication barriers. 
            The lack of widespread ISL awareness limits their access to education, employment, 
            and basic social interactions. It's time to change this.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <Card 
              key={index} 
              className="p-6 bg-card hover:shadow-medium transition-smooth animate-fade-in border-border"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <stat.icon className={`w-12 h-12 mb-4 ${stat.color}`} />
              <h3 className="text-3xl font-bold mb-2 text-foreground">{stat.number}</h3>
              <p className="text-muted-foreground">{stat.label}</p>
            </Card>
          ))}
        </div>

        <Card className="p-8 md:p-12 bg-gradient-warm text-white shadow-medium">
          <div className="max-w-3xl mx-auto text-center">
            <h3 className="text-3xl md:text-4xl font-bold mb-6">
              The Impact of Communication Barriers
            </h3>
            <div className="space-y-4 text-lg leading-relaxed opacity-90">
              <p>
                Without proper sign language translation tools, deaf individuals struggle to:
              </p>
              <ul className="text-left list-disc list-inside space-y-3 max-w-2xl mx-auto">
                <li>Access quality education and pursue their dreams</li>
                <li>Secure meaningful employment opportunities</li>
                <li>Navigate healthcare and public services independently</li>
                <li>Build social connections and participate fully in society</li>
                <li>Express themselves freely and be understood</li>
              </ul>
              <p className="pt-4 font-semibold text-xl">
                Every person deserves the right to communicate freely. 
                ISHARA is here to make that possible.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
};

export default WhyISL;
