import { Code2, Database, Palette, Brain, Server, LineChart } from "lucide-react";
import { Card } from "@/components/ui/card";

const CourseCategories = () => {
  const categories = [
    {
      icon: Code2,
      title: "Web Development",
      description: "Master frontend and backend technologies",
      courses: "15+ courses",
    },
    {
      icon: Database,
      title: "Data Structures & Algorithms",
      description: "Ace coding interviews at top companies",
      courses: "20+ courses",
    },
    {
      icon: Brain,
      title: "Machine Learning",
      description: "Build intelligent AI-powered applications",
      courses: "12+ courses",
    },
    {
      icon: Server,
      title: "System Design",
      description: "Design scalable distributed systems",
      courses: "8+ courses",
    },
    {
      icon: Palette,
      title: "UI/UX Design",
      description: "Create beautiful user experiences",
      courses: "10+ courses",
    },
    {
      icon: LineChart,
      title: "Data Science",
      description: "Analyze data and derive insights",
      courses: "18+ courses",
    },
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Explore Popular Courses
          </h2>
          <p className="text-muted-foreground text-lg">
            Choose from our wide range of industry-relevant courses
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category, index) => (
            <Card
              key={index}
              className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer border-2 hover:border-primary group"
            >
              <div className="flex items-start gap-4">
                <div className="p-3 bg-primary/10 rounded-lg group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <category.icon className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-lg mb-2">{category.title}</h3>
                  <p className="text-muted-foreground text-sm mb-3">
                    {category.description}
                  </p>
                  <span className="text-primary text-sm font-medium">
                    {category.courses}
                  </span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CourseCategories;
