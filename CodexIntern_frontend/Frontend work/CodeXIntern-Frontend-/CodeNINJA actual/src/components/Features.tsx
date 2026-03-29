import { Award, Users, BookOpen, TrendingUp } from "lucide-react";

const Features = () => {
  const features = [
    {
      icon: Award,
      title: "Industry-Recognized Certificates",
      description: "Get certificates valued by top tech companies worldwide",
    },
    {
      icon: Users,
      title: "Expert Mentorship",
      description: "Learn from industry experts with years of experience",
    },
    {
      icon: BookOpen,
      title: "Comprehensive Curriculum",
      description: "Updated content covering latest industry trends",
    },
    {
      icon: TrendingUp,
      title: "Career Support",
      description: "Dedicated placement cell with 128% average hike",
    },
  ];

  return (
    <section className="py-20 bg-muted">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Why Choose Coding Ninjas?
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            We're committed to helping you achieve your dream tech career
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="text-center space-y-4 animate-fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="inline-flex p-4 bg-primary rounded-full">
                <feature.icon className="w-8 h-8 text-primary-foreground" />
              </div>
              <h3 className="font-bold text-xl">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
