import { Card } from "@/components/ui/card";
import { Star } from "lucide-react";

const Testimonials = () => {
  const testimonials = [
    {
      name: "Rahul Sharma",
      role: "Software Engineer at Google",
      company: "Google",
      rating: 5,
      text: "Coding Ninjas helped me land my dream job at Google. The DSA course was comprehensive and the mentors were extremely helpful.",
    },
    {
      name: "Priya Patel",
      role: "Full Stack Developer at Amazon",
      company: "Amazon",
      rating: 5,
      text: "The web development course gave me all the skills I needed. Got placed at Amazon with a 150% hike!",
    },
    {
      name: "Amit Kumar",
      role: "ML Engineer at Microsoft",
      company: "Microsoft",
      rating: 5,
      text: "Best investment in my career. The Machine Learning course is industry-grade and the placement support is outstanding.",
    },
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Success Stories from Our Students
          </h2>
          <p className="text-muted-foreground text-lg">
            See how we've helped thousands achieve their career goals
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="p-6 hover:shadow-xl transition-shadow">
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                ))}
              </div>
              <p className="text-muted-foreground mb-6 italic">
                "{testimonial.text}"
              </p>
              <div className="border-t pt-4">
                <p className="font-bold">{testimonial.name}</p>
                <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                <p className="text-sm text-primary font-medium mt-1">
                  {testimonial.company}
                </p>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
