import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";

export default function DuckLangInterpreter() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("Output will appear here...");

  const runCode = () => {
    // Mock execution (replace with real DuckLang interpreter when available)
    if (code.trim() === "print 'Hello, DuckLang!'") {
      setOutput("Hello, DuckLang!");
    } else {
      setOutput("Error: Unknown DuckLang command");
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">DuckLang Online Interpreter</h1>
      <Card>
        <CardContent className="p-4">
          <Textarea
            rows={5}
            placeholder="Write your DuckLang code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="mb-4"
          />
          <Button onClick={runCode}>Run Code</Button>
        </CardContent>
      </Card>
      <Card className="mt-4">
        <CardContent className="p-4">
          <h2 className="text-lg font-semibold">Output:</h2>
          <pre className="mt-2 bg-gray-100 p-2 rounded">{output}</pre>
        </CardContent>
      </Card>
    </div>
  );
}
