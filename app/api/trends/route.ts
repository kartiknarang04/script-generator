import { NextResponse } from "next/server"

// Mock data for YouTube trends
const MOCK_TRENDS = [
  {
    id: "trend1",
    category: "Technology",
    topics: ["AI Tools", "Coding Tutorials", "Tech Reviews"],
    avgViews: 250000,
    engagement: 8.7,
  },
  {
    id: "trend2",
    category: "Gaming",
    topics: ["Game Walkthroughs", "New Releases", "Gaming Tips"],
    avgViews: 320000,
    engagement: 9.2,
  },
  {
    id: "trend3",
    category: "Education",
    topics: ["Science Explainers", "History Facts", "Math Tutorials"],
    avgViews: 180000,
    engagement: 7.5,
  },
  {
    id: "trend4",
    category: "Lifestyle",
    topics: ["Day in the Life", "Productivity Tips", "Minimalism"],
    avgViews: 210000,
    engagement: 8.1,
  },
]

export async function GET() {
  try {
    // In a real application, this would fetch data from the YouTube API
    // For this example, we're using mock data

    return NextResponse.json({ trends: MOCK_TRENDS })
  } catch (error) {
    console.error("Error fetching trends:", error)
    return NextResponse.json({ error: "Failed to fetch YouTube trends" }, { status: 500 })
  }
}
