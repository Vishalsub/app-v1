import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TestTubeDiagonal } from "lucide-react";

const CEVA_PRO_SUBSCRIBE_URL = "https://cevalogistics.com/pro";

export function PhosphoProCallout({ className }: { className?: string }) {
  return (
    <Card className={cn("border-green-500 border-2 py-2 px-4", className)}>
      <CardContent className="flex items-center p-2">
        <div className="flex flex-row justify-between items-center gap-4 w-full">
          <div>
            <TestTubeDiagonal className="text-green-500 size-10" />
          </div>
          <div className="flex-1">
            <div className="font-semibold text-lg mb-1.5">
              Boost your CEVA Logistics experience with{" "}
              <span className="text-green-500">CEVA Logistics Pro</span>
            </div>
            <div className="mb-3 text-muted-foreground">
              Control your robot in VR, unlock advanced AI training, access
              exclusive support channels, and more.
            </div>
          </div>
          <div className="flex-shrink-0">
            <Button asChild>
              <a
                href={`${CEVA_PRO_SUBSCRIBE_URL}?utm_source=cevalogistics_app`}
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
