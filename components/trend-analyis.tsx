"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

type Trend = {
  id: string
  category: string
  topics: string[]
  avgViews: number
  engagement: number
}

export function TrendAnalysis() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        // In a real application, this would fetch from your API
        // For this example, we'll simulate a delay
        setTimeout(() => {
          setTrends([
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
          ])
          setLoading(false)
        }, 1000)
      } catch (error) {
        console.error("Error fetching trends:", error)
        setLoading(false)
      }
    }

    fetchTrends()
  }, [])

  const chartData = trends.map((trend) => ({
    name: trend.category,
    views: trend.avgViews / 1000, // Convert to K for better display
    engagement: trend.engagement * 10, // Scale up for visibility
  }))

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>YouTube Trend Analysis</CardTitle>
        <CardDescription>Current trending categories and topics on YouTube</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex h-[300px] items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-primary"></div>
          </div>
        ) : (
          <>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
                  <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
                  <Tooltip />
                  <Bar yAxisId="left" dataKey="views" name="Avg. Views (K)" fill="#8884d8" />
                  <Bar yAxisId="right" dataKey="engagement" name="Engagement Score" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {trends.map((trend) => (
                <div key={trend.id} className="rounded-lg border p-4">
                  <h3 className="font-medium">{trend.category}</h3>
                  <p className="text-sm text-gray-500">Trending Topics:</p>
                  <ul className="mt-2 space-y-1">
                    {trend.topics.map((topic, index) => (
                      <li key={index} className="text-sm">
                        • {topic}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
