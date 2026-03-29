import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card } from "@/components/ui/card";

const CourseFinderForm = () => {
  const [experience, setExperience] = useState("");

  return (
    <Card className="p-8 bg-card border-2 border-border shadow-2xl">
      <h2 className="text-2xl font-bold mb-6">Let's find the right course for you</h2>
      
      <form className="space-y-6">
        {/* Experience Selection */}
        <div className="space-y-3">
          <Label className="text-base font-semibold">Experience</Label>
          <RadioGroup value={experience} onValueChange={setExperience}>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="working-tech" id="working-tech" />
              <Label htmlFor="working-tech" className="font-normal cursor-pointer">
                Working Professional - Technical Roles
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="working-non-tech" id="working-non-tech" />
              <Label htmlFor="working-non-tech" className="font-normal cursor-pointer">
                Working Professional - Non Technical
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="final-year" id="final-year" />
              <Label htmlFor="final-year" className="font-normal cursor-pointer">
                College Student - Final Year
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="pre-final" id="pre-final" />
              <Label htmlFor="pre-final" className="font-normal cursor-pointer">
                College Student - 1st to Pre-final Year
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="others" id="others" />
              <Label htmlFor="others" className="font-normal cursor-pointer">
                Others
              </Label>
            </div>
          </RadioGroup>
        </div>

        {/* Topic Selection */}
        <div className="space-y-2">
          <Label htmlFor="topic">Select topic of interest</Label>
          <Select>
            <SelectTrigger id="topic" className="bg-background">
              <SelectValue placeholder="Select your options/choices" />
            </SelectTrigger>
            <SelectContent className="bg-card z-50">
              <SelectItem value="dsa">Data Structures & Algorithms</SelectItem>
              <SelectItem value="web">Web Development</SelectItem>
              <SelectItem value="ml">Machine Learning</SelectItem>
              <SelectItem value="system">System Design</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Name */}
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input id="name" placeholder="Enter name" className="bg-background" />
        </div>

        {/* Phone Number */}
        <div className="space-y-2">
          <Label htmlFor="phone">Phone Number</Label>
          <Input id="phone" type="tel" placeholder="Enter phone number" className="bg-background" />
        </div>

        {/* Email */}
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="Enter email" className="bg-background" />
        </div>

        {/* Submit Button */}
        <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-lg py-6">
          Find your course
        </Button>

        {/* Privacy Notice */}
        <p className="text-xs text-muted-foreground">
          I authorise Coding Ninjas to contact me with course updates & offers via Email/SMS/Whatsapp/Call. 
          I have read and agree to Privacy Policy & Terms of use
        </p>
      </form>
    </Card>
  );
};

export default CourseFinderForm;
