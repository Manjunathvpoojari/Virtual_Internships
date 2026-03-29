import { CheckCircle } from "lucide-react";
import CourseFinderForm from "./CourseFinderForm";
import heroBg from "@/assets/hero-bg.jpg";

const Hero = () => {
  const stats = [
    { text: "128% average hike", subtext: "via our placement cell" },
    { text: "1.5 Lac+ learners", subtext: "cracked top tech companies" },
    { text: "1,400+ alumni", subtext: "in MAANG & 103 unicorn startups" },
  ];

  return (
    <section className="relative bg-gradient-hero min-h-[90vh] flex items-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `url(${heroBg})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      />
      
      <div className="container mx-auto px-4 py-16 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="text-white space-y-8 animate-fade-in">
            <p className="text-accent text-sm font-medium">Restricted by opportunities?</p>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              Get the tech career you deserve. Faster.
            </h1>

            <div className="space-y-4">
              {stats.map((stat, index) => (
                <div key={index} className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-accent flex-shrink-0 mt-1" />
                  <div>
                    <span className="font-semibold">{stat.text}</span>
                    <span className="text-muted-foreground ml-1">{stat.subtext}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Content - Form */}
          <div className="animate-fade-in">
            <CourseFinderForm />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
