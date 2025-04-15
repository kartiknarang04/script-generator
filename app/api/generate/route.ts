import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(req: NextRequest) {
  try {
    const { topic, tone, length } = await req.json()

    if (!topic) {
      return NextResponse.json({ error: "Topic is required" }, { status: 400 })
    }

    const prompt = `Generate a YouTube script about "${topic}" with a ${tone} tone. 
    The script should be approximately ${length} words long and include:
    - An engaging introduction
    - Main content with key points
    - Practical tips or actionable advice
    - A conclusion with a call to action
    
    Format the script with markdown headings and sections.`

    const { text } = await generateText({
      model: openai("gpt-4o"),
      prompt,
      system:
        "You are an expert YouTube script writer who specializes in creating engaging, well-structured scripts that keep viewers watching. Your scripts are conversational, include hooks, and follow best practices for YouTube content.",
    })

    return NextResponse.json({ script: text })
  } catch (error) {
    console.error("Script generation error:", error)
    return NextResponse.json({ error: "Failed to generate script" }, { status: 500 })
  }
}
