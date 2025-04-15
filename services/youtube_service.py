import requests
import os
import json
import re
import string
from collections import Counter, defaultdict
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from datetime import datetime, timedelta
from googleapiclient.discovery import build

class YouTubeService:
    def __init__(self):
        self.api_key = os.environ.get("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # Initialize NLP components
        try:
            self.nlp = spacy.load("en_core_web_sm")
            # Extra YouTube-specific stopwords
            self.extra_stopwords = {"subscribe", "channel", "watch", "video", "instagram", "facebook", "youtube", 
                                   "official", "tv", "like", "share", "follow", "live", "new", "us", "join", "today"}
            self.stopwords = set(stopwords.words("english")).union(self.extra_stopwords)
            self.ps = PorterStemmer()
        except:
            print("Warning: NLP components not fully loaded. Advanced trend analysis may not work.")
            self.nlp = None
            self.stopwords = set()
            self.ps = None
        
        # YouTube video categories
        self.categories = {
            "0": "All",
            "1": "Film & Animation",
            "2": "Autos & Vehicles",
            "10": "Music",
            "15": "Pets & Animals",
            "17": "Sports",
            "20": "Gaming",
            "22": "People & Blogs",
            "23": "Comedy",
            "24": "Entertainment",
            "25": "News & Politics",
            "26": "Howto & Style",
            "27": "Education",
            "28": "Science & Technology"
        }
    
    def get_trending_videos(self, region_code="US", category_id="0", max_results=50):
        """
        Get trending videos from YouTube API
        """
        if not self.api_key:
            return self._get_mock_trends()
        
        try:
            youtube = build("youtube", "v3", developerKey=self.api_key, static_discovery=False)
            
            request = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                chart="mostPopular",
                regionCode=region_code.upper(),
                videoCategoryId=category_id,
                maxResults=min(50, max_results)  # YouTube allows only 50 per request
            )
            response = request.execute()
            videos = response.get("items", [])
            
            # If more needed and available
            while len(videos) < max_results and "nextPageToken" in response:
                request = youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    chart="mostPopular",
                    regionCode=region_code.upper(),
                    videoCategoryId=category_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=response["nextPageToken"]
                )
                response = request.execute()
                videos.extend(response.get("items", []))
            
            return {"items": videos[:max_results]}
            
        except Exception as e:
            print(f"Error fetching trending videos: {e}")
            return self._get_mock_trends()
    
    def get_categories(self):
        """
        Return the available YouTube categories
        """
        return self.categories
    
    def analyze_trends(self, region_code="US", max_results=50):
        """
        Analyze trending videos and extract insights using NLP
        """
        if not self.api_key or not self.nlp:
            return self._get_mock_analysis()
        
        # Get trending videos across all categories
        all_videos_response = self.get_trending_videos(region_code, "0", max_results)
        
        if "items" not in all_videos_response or not all_videos_response["items"]:
            return self._get_mock_analysis()
        
        all_videos = all_videos_response["items"]
        
        # Analyze the data
        analysis = {
            "total_videos": len(all_videos),
            "region": region_code,
            "categories": {},
            "tags": {},
            "channels": {},
            "avg_views": 0,
            "avg_likes": 0,
            "avg_comments": 0,
            "video_length": {},
            "top_videos": [],
            "trending_phrases": {}
        }
        
        total_views = 0
        total_likes = 0
        total_comments = 0
        
        # Category-specific keywords
        category_keywords = defaultdict(list)
        
        for item in all_videos:
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            
            # Category analysis
            category_id = snippet.get("categoryId", "0")
            category_name = self.categories.get(category_id, "Unknown")
            
            if category_name not in analysis["categories"]:
                analysis["categories"][category_name] = {
                    "count": 0,
                    "views": 0,
                    "likes": 0
                }
            
            analysis["categories"][category_name]["count"] += 1
            analysis["categories"][category_name]["views"] += int(stats.get("viewCount", 0))
            analysis["categories"][category_name]["likes"] += int(stats.get("likeCount", 0))
            
            # NLP Analysis
            title = self._clean_text(snippet.get("title", ""))
            description = self._clean_text(snippet.get("description", ""))
            tags = snippet.get("tags", [])
            
            # Combine text for analysis with emphasis on tags
            full_text = f"{title} {description} " + (" ".join(tags) + " ") * 3
            
            # Extract phrases
            phrases = self._extract_phrases(full_text)
            phrases = [word for word in phrases if word not in self.stopwords]
            category_keywords[category_id].extend(phrases)
            
            # Tag analysis
            for tag in tags:
                if tag not in analysis["tags"]:
                    analysis["tags"][tag] = 0
                analysis["tags"][tag] += 1
            
            # Channel analysis
            channel = snippet.get("channelTitle", "Unknown")
            if channel not in analysis["channels"]:
                analysis["channels"][channel] = 0
            analysis["channels"][channel] += 1
            
            # Stats aggregation
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            
            total_views += views
            total_likes += likes
            total_comments += comments
            
            # Video length analysis
            duration = item.get("contentDetails", {}).get("duration", "PT0M0S")
            minutes = self._parse_duration(duration)
            length_key = "0-5 min" if minutes < 5 else "5-10 min" if minutes < 10 else "10+ min"
            
            if length_key not in analysis["video_length"]:
                analysis["video_length"][length_key] = 0
            analysis["video_length"][length_key] += 1
            
            # Top videos
            analysis["top_videos"].append({
                "title": snippet.get("title", "Unknown"),
                "channel": snippet.get("channelTitle", "Unknown"),
                "views": views,
                "likes": likes,
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                "video_id": item.get("id", ""),
                "tags": tags,
                "category_id": category_id,
                "category_name": category_name,
                "description": snippet.get("description", "")
            })
        
        # Calculate averages
        if analysis["total_videos"] > 0:
            analysis["avg_views"] = total_views // analysis["total_videos"]
            analysis["avg_likes"] = total_likes // analysis["total_videos"]
            analysis["avg_comments"] = total_comments // analysis["total_videos"]
        
        # Process category keywords
        for cat_id, words in category_keywords.items():
            if words:
                counts = self._stem_keywords(words)
                top_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:15]
                cat_name = self.categories.get(cat_id, f"Category {cat_id}")
                analysis["trending_phrases"][cat_name] = dict(top_words)
        
        # Sort tags by frequency and limit to top 20
        analysis["tags"] = dict(sorted(analysis["tags"].items(), key=lambda x: x[1], reverse=True)[:20])
        
        # Sort channels by frequency and limit to top 10
        analysis["channels"] = dict(sorted(analysis["channels"].items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Sort top videos by views
        analysis["top_videos"] = sorted(analysis["top_videos"], key=lambda x: x["views"], reverse=True)[:10]
        
        return analysis
    
    def _clean_text(self, text):
        """Clean text for NLP processing"""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[\r\n]+", " ", text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    def _extract_phrases(self, text):
        """Extract noun phrases from text using spaCy"""
        if not self.nlp:
            return []
        doc = self.nlp(text)
        return [chunk.text.lower() for chunk in doc.noun_chunks if chunk.text.lower() not in self.stopwords]
    
    def _stem_keywords(self, keywords):
        """Group similar keywords by stemming"""
        if not self.ps:
            return Counter(keywords)
            
        stem_map = defaultdict(list)
        for word in keywords:
            root = self.ps.stem(word)
            stem_map[root].append(word)
        
        # Use the shortest word in each stem group as the representative
        final_counts = {min(set(v), key=len): len(v) for k, v in stem_map.items() if len(v) > 1}
        
        # Add words that didn't have duplicates
        for word in keywords:
            root = self.ps.stem(word)
            if len(stem_map[root]) <= 1:
                final_counts[word] = 1
                
        return final_counts
    
    def _parse_duration(self, duration):
        """
        Parse ISO 8601 duration format to minutes
        Example: PT1H30M15S -> 90.25 minutes
        """
        minutes = 0
        
        # Hours
        h_pos = duration.find('H')
        if h_pos > 0:
            h_str = duration[duration.find('T')+1:h_pos]
            minutes += int(h_str) * 60
        
        # Minutes
        m_pos = duration.find('M')
        if m_pos > 0:
            start_pos = h_pos + 1 if h_pos > 0 else duration.find('T') + 1
            m_str = duration[start_pos:m_pos]
            minutes += int(m_str)
        
        return minutes
    
    def _get_mock_trends(self):
        """
        Return mock trending videos when API key is not available
        """
        return {
            "items": [
                {
                    "id": "video1",
                    "snippet": {
                        "title": "How to Build a Website in 2025",
                        "channelTitle": "Tech Tutorials",
                        "publishedAt": "2025-04-10T14:30:00Z",
                        "categoryId": "28",
                        "tags": ["web development", "coding", "html", "css"],
                        "description": "Learn how to build a modern website from scratch using the latest technologies.",
                        "thumbnails": {
                            "medium": {
                                "url": "https://via.placeholder.com/320x180"
                            }
                        }
                    },
                    "statistics": {
                        "viewCount": "250000",
                        "likeCount": "15000",
                        "commentCount": "1200"
                    },
                    "contentDetails": {
                        "duration": "PT15M30S"
                    }
                },
                {
                    "id": "video2",
                    "snippet": {
                        "title": "10 Productivity Hacks You Need to Know",
                        "channelTitle": "Life Optimized",
                        "publishedAt": "2025-04-08T09:15:00Z",
                        "categoryId": "22",
                        "tags": ["productivity", "time management", "habits"],
                        "description": "Boost your productivity with these 10 simple but effective hacks.",
                        "thumbnails": {
                            "medium": {
                                "url": "https://via.placeholder.com/320x180"
                            }
                        }
                    },
                    "statistics": {
                        "viewCount": "180000",
                        "likeCount": "12000",
                        "commentCount": "800"
                    },
                    "contentDetails": {
                        "duration": "PT8M45S"
                    }
                },
                {
                    "id": "video3",
                    "snippet": {
                        "title": "The Future of AI in Content Creation",
                        "channelTitle": "AI Insights",
                        "publishedAt": "2025-04-05T16:45:00Z",
                        "categoryId": "28",
                        "tags": ["artificial intelligence", "content creation", "future tech"],
                        "description": "Discover how AI is revolutionizing content creation and what it means for creators.",
                        "thumbnails": {
                            "medium": {
                                "url": "https://via.placeholder.com/320x180"
                            }
                        }
                    },
                    "statistics": {
                        "viewCount": "320000",
                        "likeCount": "18000",
                        "commentCount": "1500"
                    },
                    "contentDetails": {
                        "duration": "PT12M15S"
                    }
                }
            ]
        }
    
    def _get_mock_analysis(self):
        """
        Return mock trend analysis when API key is not available
        """
        return {
            "total_videos": 50,
            "region": "US",
            "categories": {
                "Entertainment": {"count": 15, "views": 5000000, "likes": 350000},
                "Gaming": {"count": 10, "views": 3000000, "likes": 250000},
                "Music": {"count": 8, "views": 4000000, "likes": 300000},
                "Education": {"count": 7, "views": 1500000, "likes": 120000},
                "Science & Technology": {"count": 5, "views": 2000000, "likes": 180000},
                "Howto & Style": {"count": 5, "views": 1800000, "likes": 150000}
            },
            "tags": {
                "gaming": 12,
                "tutorial": 10,
                "music": 8,
                "review": 7,
                "howto": 6,
                "tech": 6,
                "news": 5,
                "comedy": 5,
                "vlog": 4,
                "reaction": 4
            },
            "channels": {
                "Popular Gaming Channel": 3,
                "Music Videos Official": 2,
                "Tech Reviews": 2,
                "Educational Content": 2,
                "Daily Vlogs": 1
            },
            "avg_views": 250000,
            "avg_likes": 15000,
            "avg_comments": 1200,
            "video_length": {
                "0-5 min": 10,
                "5-10 min": 25,
                "10+ min": 15
            },
            "trending_phrases": {
                "Entertainment": {"viral challenge": 15, "celebrity interview": 12, "behind scenes": 10},
                "Gaming": {"gameplay walkthrough": 14, "new release": 11, "tips tricks": 9},
                "Technology": {"product review": 13, "how to": 11, "tutorial": 8}
            },
            "top_videos": [
                {
                    "title": "How to Build a Website in 2025",
                    "channel": "Tech Tutorials",
                    "views": 250000,
                    "likes": 15000,
                    "thumbnail": "https://via.placeholder.com/320x180",
                    "video_id": "video1",
                    "tags": ["web development", "coding", "html", "css"],
                    "category_id": "28",
                    "category_name": "Science & Technology",
                    "description": "Learn how to build a modern website from scratch using the latest technologies."
                },
                {
                    "title": "10 Productivity Hacks You Need to Know",
                    "channel": "Life Optimized",
                    "views": 180000,
                    "likes": 12000,
                    "thumbnail": "https://via.placeholder.com/320x180",
                    "video_id": "video2",
                    "tags": ["productivity", "time management", "habits"],
                    "category_id": "22",
                    "category_name": "People & Blogs",
                    "description": "Boost your productivity with these 10 simple but effective hacks."
                },
                {
                    "title": "The Future of AI in Content Creation",
                    "channel": "AI Insights",
                    "views": 320000,
                    "likes": 18000,
                    "thumbnail": "https://via.placeholder.com/320x180",
                    "video_id": "video3",
                    "tags": ["artificial intelligence", "content creation", "future tech"],
                    "category_id": "28",
                    "category_name": "Science & Technology",
                    "description": "Discover how AI is revolutionizing content creation and what it means for creators."
                }
            ]
        }
