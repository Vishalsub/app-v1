import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TestTubeDiagonal } from "lucide-react";

const CEVA_VR_SUBSCRIBE_URL = "https://cevalogistics.com/vr";

export function CEVAVRCallout({ className }: { className?: string }) {
  return (
    <Card className={cn("border-blue-500 border-2 py-2 px-4", className)}>
      <CardContent className="flex items-center p-2">
        <div className="flex flex-row justify-between items-center gap-4 w-full">
          <div>
            <TestTubeDiagonal className="text-blue-600 size-10" />
          </div>
          <div className="flex-1">
            <div className="font-semibold text-lg mb-1.5">
              Experience CEVA Logistics in{" "}
              <span className="text-blue-600">Virtual Reality</span>
            </div>
            <div className="mb-3 text-muted-foreground">
              Control your robot with immersive VR technology, enhanced precision,
              and intuitive hand tracking for advanced logistics operations.
            </div>
          </div>
          <div className="flex-shrink-0">
            <Button asChild>
              <a
                href={`${CEVA_VR_SUBSCRIBE_URL}?utm_source=cevalogistics_app`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Learn More
              </a>
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}


