import Link from "next/link"
import { ArrowRight, Youtube } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center">
          <div className="flex items-center gap-2 font-bold">
            <Youtube className="h-6 w-6 text-red-600" />
            <span>ScriptGenius</span>
          </div>
          <nav className="ml-auto flex gap-4">
            <Link href="/dashboard" className="text-sm font-medium">
              Dashboard
            </Link>
            <Link href="/login" className="text-sm font-medium">
              Login
            </Link>
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
                  AI-Powered YouTube Script Generator
                </h1>
                <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl">
                  Generate engaging YouTube scripts in seconds using advanced AI. Analyze trends and create content that
                  resonates with your audience.
                </p>
              </div>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Button asChild>
                  <Link href="/dashboard">
                    Get Started <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href="/about">Learn More</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
          <div className="container px-4 md:px-6">
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3">
              <Card>
                <CardHeader>
                  <CardTitle>Lightning Fast</CardTitle>
                  <CardDescription>Generate 2,000+ words in under 10 seconds</CardDescription>
                </CardHeader>
                <CardContent>
                  <p>
                    Our AI engine powered by Mistral 7B delivers high-quality scripts instantly, saving you hours of
                    writing time.
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Trend Analysis</CardTitle>
                  <CardDescription>Powered by YouTube API</CardDescription>
                </CardHeader>
                <CardContent>
                  <p>
                    Analyze over 1 million videos to identify trending topics and content ideas that resonate with
                    viewers.
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Full Control</CardTitle>
                  <CardDescription>Customizable dashboard</CardDescription>
                </CardHeader>
                <CardContent>
                  <p>
                    Adjust tone, style, length, and more with our intuitive dashboard for complete creative control.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </main>
      <footer className="border-t py-6 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <p className="text-sm text-gray-500">© 2025 ScriptGenius. All rights reserved.</p>
          <nav className="flex gap-4 sm:gap-6">
            <Link href="/terms" className="text-sm font-medium">
              Terms
            </Link>
            <Link href="/privacy" className="text-sm font-medium">
              Privacy
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  )
}
