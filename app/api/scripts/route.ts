import { type NextRequest, NextResponse } from "next/server"

// Mock data for user scripts
const MOCK_SCRIPTS = [
  {
    id: "script1",
    title: "How to Build a Website in 2025",
    createdAt: "2025-04-10T14:30:00Z",
    length: 1850,
    tone: "educational",
  },
  {
    id: "script2",
    title: "10 Productivity Hacks You Need to Know",
    createdAt: "2025-04-08T09:15:00Z",
    length: 1200,
    tone: "informative",
  },
  {
    id: "script3",
    title: "The Future of AI in Content Creation",
    createdAt: "2025-04-05T16:45:00Z",
    length: 2100,
    tone: "professional",
  },
]

export async function GET() {
  try {
    // In a real application, this would fetch data from MongoDB
    // For this example, we're using mock data

    return NextResponse.json({ scripts: MOCK_SCRIPTS })
  } catch (error) {
    console.error("Error fetching scripts:", error)
    return NextResponse.json({ error: "Failed to fetch scripts" }, { status: 500 })
  }
}

export async function POST(req: NextRequest) {
  try {
    const { title, content, tone, length } = await req.json()

    if (!title || !content) {
      return NextResponse.json({ error: "Title and content are required" }, { status: 400 })
    }

    // In a real application, this would save to MongoDB
    // For this example, we'll just return a success response

    return NextResponse.json({
      success: true,
      script: {
        id: `script${Date.now()}`,
        title,
        createdAt: new Date().toISOString(),
        length: content.split(" ").length,
        tone,
      },
    })
  } catch (error) {
    console.error("Error saving script:", error)
    return NextResponse.json({ error: "Failed to save script" }, { status: 500 })
  }
}
