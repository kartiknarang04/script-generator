"use client"

import { useState } from "react"
import { Youtube, Sparkles, TrendingUp, Settings, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import {
  SidebarProvider,
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar"

export default function Dashboard() {
  const [generatedScript, setGeneratedScript] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [scriptLength, setScriptLength] = useState([1000])
  const [topic, setTopic] = useState("")
  const [tone, setTone] = useState("informative")

  const generateScript = async () => {
    if (!topic) return

    setIsGenerating(true)
    setGeneratedScript("")

    // Simulate API call with timeout
    setTimeout(() => {
      const script = `# ${topic.toUpperCase()} - YouTube Script

## Introduction
Hey everyone, welcome back to the channel! Today we're diving deep into ${topic}, something I've been really excited to share with you all.

## Main Content
${topic} has been gaining a lot of attention lately, and for good reason. Let's break down why this matters and how you can benefit from understanding it better.

First, let's talk about the basics. ${topic} is fundamentally about connecting ideas and creating value through innovative approaches. Many creators overlook the importance of this concept, but it's absolutely crucial for growth in today's landscape.

One of the most interesting aspects of ${topic} is how it relates to audience engagement. Studies have shown that channels focusing on this area see up to 40% higher retention rates and significantly better comment activity.

## Practical Tips
Here are three actionable tips you can implement today:

1. Start by analyzing your current content strategy and identify areas where ${topic} could be better integrated
2. Experiment with different presentation styles to see what resonates best with your specific audience
3. Create a feedback loop where you can measure the impact of these changes on your channel metrics

## Conclusion
That's it for today's video on ${topic}! If you found this helpful, please hit that like button and subscribe for more content like this. Drop your questions in the comments below, and I'll see you in the next one!`

      setGeneratedScript(script)
      setIsGenerating(false)
    }, 2000)
  }

  return (
    <SidebarProvider>
      <div className="flex min-h-screen">
        <Sidebar>
          <SidebarHeader>
            <div className="flex items-center gap-2 px-4 py-2">
              <Youtube className="h-6 w-6 text-red-600" />
              <span className="font-bold">ScriptGenius</span>
            </div>
          </SidebarHeader>
          <SidebarContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton isActive>
                  <Sparkles className="h-4 w-4" />
                  <span>Generate</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton>
                  <TrendingUp className="h-4 w-4" />
                  <span>Trend Analysis</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton>
                  <Settings className="h-4 w-4" />
                  <span>Settings</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarContent>
          <SidebarFooter>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton>
                  <LogOut className="h-4 w-4" />
                  <span>Logout</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarFooter>
        </Sidebar>
        <div className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-6">Script Generator</h1>
          <Tabs defaultValue="generate">
            <TabsList className="mb-4">
              <TabsTrigger value="generate">Generate</TabsTrigger>
              <TabsTrigger value="history">History</TabsTrigger>
            </TabsList>
            <TabsContent value="generate" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Script Parameters</CardTitle>
                  <CardDescription>Configure your script generation settings</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="topic">Topic or Title</Label>
                    <Input
                      id="topic"
                      placeholder="Enter your video topic or title"
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="tone">Tone</Label>
                    <select
                      id="tone"
                      className="w-full rounded-md border border-input bg-background px-3 py-2"
                      value={tone}
                      onChange={(e) => setTone(e.target.value)}
                    >
                      <option value="informative">Informative</option>
                      <option value="entertaining">Entertaining</option>
                      <option value="educational">Educational</option>
                      <option value="conversational">Conversational</option>
                      <option value="professional">Professional</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label htmlFor="length">Script Length (words)</Label>
                      <span>{scriptLength[0]}</span>
                    </div>
                    <Slider
                      id="length"
                      min={500}
                      max={3000}
                      step={100}
                      value={scriptLength}
                      onValueChange={setScriptLength}
                    />
                  </div>
                  <Button className="w-full" onClick={generateScript} disabled={isGenerating || !topic}>
                    {isGenerating ? "Generating..." : "Generate Script"}
                  </Button>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Generated Script</CardTitle>
                  <CardDescription>Your AI-generated YouTube script</CardDescription>
                </CardHeader>
                <CardContent>
                  {generatedScript ? (
                    <Textarea
                      className="min-h-[300px] font-mono"
                      value={generatedScript}
                      onChange={(e) => setGeneratedScript(e.target.value)}
                    />
                  ) : (
                    <div className="flex h-[300px] items-center justify-center text-gray-500">
                      {isGenerating ? (
                        <div className="flex flex-col items-center gap-2">
                          <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-primary"></div>
                          <p>Generating your script...</p>
                        </div>
                      ) : (
                        "Configure parameters and click Generate to create your script"
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="history">
              <Card>
                <CardHeader>
                  <CardTitle>Script History</CardTitle>
                  <CardDescription>Your previously generated scripts</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-center py-8 text-gray-500">No previous scripts found</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </SidebarProvider>
  )
}
