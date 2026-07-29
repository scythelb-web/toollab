"""
ToolLab Blog — SEO-optimized articles targeting high-volume keywords.
Articles are stored inline — no database, no markdown parser needed.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from context import ctx

router = APIRouter()

ARTICLES = {
    "convert-pdf-to-word-free": {
        "title": "Convert PDF to Word Free Online — No Signup, No Watermarks",
        "description": "Convert any PDF to an editable Word document free, right in your browser. No signup, no watermarks, no file size limits. Fast and private.",
        "date": "2026-07-15",
        "category": "pdf",
        "keywords": "convert pdf to word, pdf to docx, free pdf converter, pdf to word online",
        "content": """
<p>Need to edit a PDF but stuck with a read-only file? Converting PDF to Word is the fastest way to make those changes, and you don't need expensive software to do it.</p>

<h2>Why Convert PDF to Word?</h2>
<p>PDFs are great for sharing — they look the same on every device. But they're terrible for editing. Whether you're updating a contract, fixing a typo in a report, or extracting text from a scanned document, converting to Word (.docx) gives you full editing control.</p>

<h2>How ToolLab's PDF to Word Converter Works</h2>
<ol>
  <li><strong>Upload your PDF</strong> — drag and drop or click to browse</li>
  <li><strong>Click convert</strong> — we extract all text from every page</li>
  <li><strong>Download your .docx file</strong> — open in Word, Google Docs, or LibreOffice</li>
</ol>
<p>The whole process takes seconds. Your file stays on our server only during processing — we don't store or read your documents.</p>

<h2>Features</h2>
<ul>
  <li><strong>100% free</strong> — no credit card, no trial period, no watermarks</li>
  <li><strong>No signup required</strong> — just upload and convert</li>
  <li><strong>Private & secure</strong> — files are deleted immediately after processing</li>
  <li><strong>Preserves text structure</strong> — headings, paragraphs, and page breaks are maintained</li>
  <li><strong>Works with large files</strong> — handles PDFs up to 50MB</li>
</ul>

<h2>Other Free PDF Tools</h2>
<p>ToolLab offers a full suite of PDF tools — all free:</p>
<ul>
  <li><a href="/pdf/merge">Merge PDF files</a> — combine multiple PDFs into one</li>
  <li><a href="/pdf/compress">Compress PDF</a> — reduce file size without losing quality</li>
  <li><a href="/pdf/split">Split PDF</a> — extract pages into separate files</li>
  <li><a href="/pdf/rotate">Rotate PDF</a> — fix sideways scans in one click</li>
</ul>

<p>Ready to convert? <a href="/pdf/to-word">Try the PDF to Word converter now →</a></p>
"""
    },

    "remove-background-from-image-free": {
        "title": "Remove Background from Image Free — Instant, No Signup",
        "description": "Remove image backgrounds instantly with AI. No Photoshop needed, no signup required. Download transparent PNGs free. Works with photos, products, and logos.",
        "date": "2026-07-16",
        "category": "image",
        "keywords": "remove background from image, background remover free, remove bg, transparent background maker",
        "content": """
<p>Need a transparent background for a product photo, profile picture, or logo? AI background removal has gotten incredibly good — and it's now completely free at ToolLab.</p>

<h2>How AI Background Removal Works</h2>
<p>Our background remover uses a machine learning model called REMBG that's been trained on millions of images. It identifies the main subject in your photo — a person, product, animal, or object — and separates it from the background in under a second.</p>

<h2>How to Remove a Background</h2>
<ol>
  <li><strong>Upload your image</strong> — JPG, PNG, or WebP</li>
  <li><strong>Wait 2-3 seconds</strong> — AI does the work</li>
  <li><strong>Download your PNG</strong> — with a clean transparent background</li>
</ol>

<h2>What It Works Best On</h2>
<ul>
  <li><strong>Product photos</strong> — perfect for eBay, Shopify, Etsy listings</li>
  <li><strong>Portraits & selfies</strong> — great for profile pictures and LinkedIn</li>
  <li><strong>Logos & icons</strong> — extract clean shapes for design work</li>
  <li><strong>Pets & animals</strong> — surprisingly good with fur and hair</li>
</ul>

<h2>Other Free Image Tools on ToolLab</h2>
<ul>
  <li><a href="/image/upscale">Image Upscaler</a> — enlarge images 2x or 4x with AI</li>
  <li><a href="/image/convert">Image Converter</a> — PNG to JPG, WebP, and more</li>
  <li><a href="/image/resize">Image Resizer</a> — resize by dimensions or percentage</li>
</ul>

<p><a href="/image/remove-bg">Remove your image background now →</a></p>
"""
    },

    "merge-pdf-files-free": {
        "title": "Merge PDF Files Free — Combine Multiple PDFs Online",
        "description": "Combine multiple PDF files into one document free. No signup, no watermarks, no page limits. Merge PDFs in any order — fast and private.",
        "date": "2026-07-17",
        "category": "pdf",
        "keywords": "merge pdf, combine pdf files, pdf merger free, join pdf online",
        "content": """
<p>Got multiple PDFs that should be one document? Whether it's chapters of a report, scanned pages from different sessions, or contracts that need combining — merging PDFs should be fast, free, and private.</p>

<h2>How PDF Merging Works at ToolLab</h2>
<ol>
  <li><strong>Upload your PDFs</strong> — select as many files as you need (up to 50MB each)</li>
  <li><strong>Arrange the order</strong> — files are merged in the order you upload them</li>
  <li><strong>Click merge</strong> — your combined PDF downloads instantly</li>
</ol>

<h2>When to Merge PDFs</h2>
<ul>
  <li><strong>Reports & proposals</strong> — combine chapters written separately</li>
  <li><strong>Scanned documents</strong> — join pages from multiple scanning sessions</li>
  <li><strong>Invoices & receipts</strong> — bundle monthly statements for accounting</li>
  <li><strong>Portfolios</strong> — create one file from multiple work samples</li>
  <li><strong>Study materials</strong> — combine lecture slides and notes into one PDF</li>
</ul>

<h2>Why ToolLab's Merger?</h2>
<ul>
  <li><strong>No file limit</strong> — merge as many PDFs as you want in one go</li>
  <li><strong>No watermarks</strong> — your output is clean and professional</li>
  <li><strong>Preserves quality</strong> — no compression or degradation</li>
  <li><strong>Private</strong> — files are deleted after processing</li>
  <li><strong>Works everywhere</strong> — Windows, Mac, Linux, iOS, Android</li>
</ul>

<p><a href="/pdf/merge">Merge your PDFs now →</a></p>
"""
    },

    "free-text-to-speech-online": {
        "title": "Free Text to Speech Online — Natural AI Voices, No Signup",
        "description": "Convert text to natural-sounding speech free. Multiple AI voices available. No account needed — just paste your text and download MP3 audio instantly.",
        "date": "2026-07-18",
        "category": "voice",
        "keywords": "text to speech free, free tts, ai voice generator, text to mp3",
        "content": """
<p>Need to turn text into spoken audio? AI text-to-speech has come a long way — voices now sound natural and expressive, not robotic. And with ToolLab's BYOK model, you can use your own OpenAI key for premium voices at cost.</p>

<h2>How Text to Speech Works</h2>
<ol>
  <li><strong>Paste your text</strong> — up to 4,096 characters</li>
  <li><strong>Pick a voice</strong> — Alloy, Echo, Fable, Onyx, Nova, or Shimmer</li>
  <li><strong>Click generate</strong> — download your MP3 in seconds</li>
</ol>

<h2>Available AI Voices</h2>
<ul>
  <li><strong>Alloy</strong> — neutral, balanced — great for general narration</li>
  <li><strong>Echo</strong> — warm, deeper tone — good for storytelling</li>
  <li><strong>Fable</strong> — expressive, British accent — perfect for creative content</li>
  <li><strong>Onyx</strong> — deep, authoritative — ideal for presentations</li>
  <li><strong>Nova</strong> — friendly, upbeat — great for tutorials and explainers</li>
  <li><strong>Shimmer</strong> — clear, conversational — good for podcasts</li>
</ul>

<h2>Use Cases</h2>
<ul>
  <li><strong>Content creators</strong> — generate voiceovers for videos and reels</li>
  <li><strong>Accessibility</strong> — convert articles and documents to audio</li>
  <li><strong>Language learners</strong> — hear correct pronunciation of written text</li>
  <li><strong>Podcasters</strong> — create intro/outro segments</li>
  <li><strong>E-learning</strong> — narrate course materials and tutorials</li>
</ul>

<h2>BYOK — You Control the Cost</h2>
<p>ToolLab uses your OpenAI API key for TTS. OpenAI charges $0.015 per 1,000 characters — that means a full article costs about 5-10 cents to convert. You get premium quality at cost, and we never see your key or your content.</p>

<p><a href="/voice/tts">Try text to speech now →</a></p>
"""
    },

    "compress-pdf-free-online": {
        "title": "Compress PDF Free Online — Reduce File Size Instantly",
        "description": "Reduce PDF file size without losing quality. Free online PDF compression — no signup, no watermarks. Perfect for email attachments and uploads.",
        "date": "2026-07-19",
        "category": "pdf",
        "keywords": "compress pdf, reduce pdf size, pdf compressor free, shrink pdf online",
        "content": """
<p>PDF too big to email? Upload rejected because the file exceeds the size limit? PDF compression solves this instantly — and it doesn't have to cost anything.</p>

<h2>How PDF Compression Works</h2>
<ol>
  <li><strong>Upload your PDF</strong> — any size up to 50MB</li>
  <li><strong>Click compress</strong> — we optimize content streams on every page</li>
  <li><strong>Download the smaller file</strong> — same content, smaller size</li>
</ol>

<h2>When to Compress PDFs</h2>
<ul>
  <li><strong>Email attachments</strong> — Gmail limits attachments to 25MB</li>
  <li><strong>Job applications</strong> — many portals have 5-10MB upload limits</li>
  <li><strong>Web uploads</strong> — faster upload speeds, less bandwidth</li>
  <li><strong>Document storage</strong> — save cloud storage space on Drive or Dropbox</li>
  <li><strong>Client deliverables</strong> — send professional documents that load fast</li>
</ul>

<h2>How Much Can You Save?</h2>
<p>Compression results vary by content:</p>
<ul>
  <li><strong>Text-heavy PDFs:</strong> 20-40% size reduction</li>
  <li><strong>Image-heavy PDFs:</strong> 10-30% (images already compressed)</li>
  <li><strong>Scanned PDFs:</strong> 15-35% (depends on scan resolution)</li>
</ul>

<h2>Privacy First</h2>
<p>Your documents are processed in memory and deleted immediately. We never store, read, or share your files. The entire process happens on our secure server and the output goes directly to your download folder.</p>

<p><a href="/pdf/compress">Compress your PDF now →</a></p>
"""
    },

    "image-upscaler-free": {
        "title": "Free AI Image Upscaler — Enlarge Photos Without Losing Quality",
        "description": "Upscale images 2x or 4x free online. Enlarge photos while preserving sharpness — no signup, no watermarks. Perfect for printing and presentations.",
        "date": "2026-07-20",
        "category": "image",
        "keywords": "image upscaler free, ai upscale image, enlarge photo without losing quality, photo enlarger online",
        "content": """
<p>Got a small image that needs to be bigger? Blowing up a photo usually makes it pixelated and blurry — but with Lanczos resampling, you can enlarge images while keeping them surprisingly sharp.</p>

<h2>How Image Upscaling Works</h2>
<ol>
  <li><strong>Upload your image</strong> — JPG, PNG, or WebP</li>
  <li><strong>Choose your scale</strong> — 2x, 3x, or 4x enlargement</li>
  <li><strong>Download the larger image</strong> — crisp and clean</li>
</ol>

<h2>When You Need Upscaling</h2>
<ul>
  <li><strong>Printing photos</strong> — a 1000px image prints at ~3 inches; upscale to 4000px for 12-inch prints</li>
  <li><strong>Presentations & slides</strong> — small logos and screenshots blown up for big screens</li>
  <li><strong>Social media</strong> — profile pictures and banners that need higher resolution</li>
  <li><strong>E-commerce</strong> — product photos that need to fill larger display areas</li>
  <li><strong>Graphic design</strong> — stock images that need more pixels for layouts</li>
</ul>

<h2>Lanczos vs Basic Resize</h2>
<p>ToolLab uses Lanczos resampling — the same algorithm used in professional software like Photoshop and GIMP. Unlike basic nearest-neighbor or bilinear resizing, Lanczos preserves edge sharpness and reduces the "soft" look you get with simpler methods.</p>

<h2>Other Image Tools</h2>
<ul>
  <li><a href="/image/remove-bg">Background Remover</a> — AI-powered, instant results</li>
  <li><a href="/image/convert">Format Converter</a> — PNG, JPG, WebP, and more</li>
  <li><a href="/image/resize">Image Resizer</a> — precise dimensions or percentage</li>
</ul>

<p><a href="/image/upscale">Upscale your image now →</a></p>
"""
    },

    "speech-to-text-free": {
        "title": "Free Speech to Text — Convert Audio to Text Instantly",
        "description": "Transcribe audio and video files to text free online. AI-powered speech recognition — no signup, fast results. Supports MP3, WAV, MP4, and more.",
        "date": "2026-07-21",
        "category": "voice",
        "keywords": "speech to text free, transcribe audio to text, free transcription, audio to text converter",
        "content": """
<p>Need to transcribe an interview, meeting recording, or voice memo? AI speech recognition has gotten remarkably accurate — and with ToolLab, you can transcribe audio files for just the cost of the OpenAI API.</p>

<h2>How Speech to Text Works</h2>
<ol>
  <li><strong>Upload your audio file</strong> — MP3, WAV, MP4, M4A, WebM</li>
  <li><strong>Click transcribe</strong> — OpenAI Whisper processes your file</li>
  <li><strong>Get your text</strong> — copy, download, or use it directly</li>
</ol>

<h2>What It's Great For</h2>
<ul>
  <li><strong>Meeting notes</strong> — transcribe recordings instead of taking manual notes</li>
  <li><strong>Interviews</strong> — journalists and researchers: turn recorded interviews into searchable text</li>
  <li><strong>Lectures & classes</strong> — convert recorded lectures into study notes</li>
  <li><strong>Content creation</strong> — transcribe podcast episodes for show notes and blog posts</li>
  <li><strong>Voice memos</strong> — turn quick thoughts into actionable text</li>
  <li><strong>Accessibility</strong> — generate captions and transcripts for video content</li>
</ul>

<h2>BYOK — Pay Only for What You Use</h2>
<p>ToolLab uses your OpenAI API key for transcription. Whisper costs $0.006 per minute of audio — a 30-minute interview costs about 18 cents to transcribe. You get state-of-the-art accuracy at cost, and your key (and content) stays private.</p>

<h2>Supported Formats</h2>
<p>MP3, MP4, MPEG, MPGA, M4A, WAV, and WebM files are all supported. Maximum file size is 25MB — that's roughly 2-3 hours of compressed audio.</p>

<p><a href="/voice/stt">Transcribe audio now →</a></p>
"""
    },

    "qr-code-generator-free": {
        "title": "Free QR Code Generator — Create QR Codes Instantly",
        "description": "Generate custom QR codes free online. No signup, no watermarks. Create QR codes for URLs, text, WiFi, and more. Download as high-resolution PNG.",
        "date": "2026-07-22",
        "category": "qr",
        "keywords": "qr code generator free, create qr code, free qr maker, qr code online",
        "content": """
<p>QR codes are everywhere — restaurant menus, event tickets, WiFi passwords, payment links. Creating one should be instant, free, and require no account. That's exactly what ToolLab's QR generator does.</p>

<h2>How to Create a QR Code</h2>
<ol>
  <li><strong>Enter your content</strong> — a URL, text, or any string</li>
  <li><strong>Click generate</strong> — your QR code appears instantly</li>
  <li><strong>Download as PNG</strong> — high resolution, ready to use anywhere</li>
</ol>

<h2>What You Can Encode</h2>
<ul>
  <li><strong>Website URLs</strong> — link to your site, portfolio, or social media</li>
  <li><strong>WiFi credentials</strong> — let guests scan to connect (use format: WIFI:S:MyNetwork;T:WPA;P:password;;)</li>
  <li><strong>Contact info</strong> — vCard format for digital business cards</li>
  <li><strong>Plain text</strong> — messages, instructions, coupon codes</li>
  <li><strong>Payment links</strong> — Venmo, PayPal, or Stripe payment pages</li>
</ul>

<h2>QR Code Best Practices</h2>
<ul>
  <li><strong>Test before printing</strong> — scan with multiple phones to verify</li>
  <li><strong>Keep URLs short</strong> — shorter URLs make simpler, more scannable QR codes</li>
  <li><strong>Add a label</strong> — tell people what scanning does ("Scan for WiFi")</li>
  <li><strong>Mind the contrast</strong> — dark QR on light background scans best</li>
</ul>

<p><a href="/qr">Generate a QR code now →</a></p>
"""
    },
}


@router.get("/", response_class=HTMLResponse)
async def blog_index(request: Request):
    """Blog listing page — all articles sorted by date (newest first)."""
    articles = sorted(
        [{"slug": slug, **article} for slug, article in ARTICLES.items()],
        key=lambda a: a["date"],
        reverse=True,
    )
    return request.app.state.templates.TemplateResponse(
        "blog_index.html", ctx(request, articles=articles)
    )


@router.get("/{slug}", response_class=HTMLResponse)
async def blog_article(request: Request, slug: str):
    """Individual blog article page."""
    article = ARTICLES.get(slug)
    if not article:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/blog", status_code=303)

    return request.app.state.templates.TemplateResponse(
        "blog_article.html",
        ctx(
            request,
            article=article,
            slug=slug,
            meta_desc=article["description"],
        ),
    )
