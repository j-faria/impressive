TopLeft, BottomLeft, TopRight, BottomRight, TopCenter, BottomCenter = range(6)
NoCache, MemCache, CompressedCache, FileCache, PersistentCache = range(5)  # for CacheMode
Off, First, Last = range(3)  # for AutoOverview

# You may change the following lines to modify the default settings
Verbose = False
Fullscreen = True
FakeFullscreen = False
Scaling = False
Supersample = None
BackgroundRendering = True
PDFRendererPath = None
UseAutoScreenSize = True
ScreenWidth = 1024
ScreenHeight = 768
WindowPos = None
TransitionDuration = 1000
MouseHideDelay = 3000
BoxFadeDuration = 100
ZoomDuration = 250
BlankFadeDuration = 250
BoxFadeBlur = 1.5
BoxFadeDarkness = 0.25
BoxFadeDarknessStep = 0.05
MarkColor = (1.0, 0.0, 0.0, 0.1)
BoxEdgeSize = 4
SpotRadius = 64
MinSpotDetail = 13
SpotDetail = 12
CacheMode = FileCache
HighQualityOverview = True
OverviewBorder = 3
OverviewLogoBorder = 24
AutoOverview = Off
InitialPage = None
Wrap = False
AutoAdvance = None
AutoAutoAdvance = False
RenderToDirectory = None
Rotation = 0
DAR = None
PAR = 1.0
Overscan = 3
PollInterval = 0
PageRangeStart = 0
PageRangeEnd = 999999
FontSize = 14
FontTextureWidth = 512
FontTextureHeight = 256
Gamma = 1.0
BlackLevel = 0
GammaStep = 1.1
BlackLevelStep = 8
EstimatedDuration = None
PageProgress = False
AutoAdvanceProgress = False
ProgressBarSizeFactor = 0.02
ProgressBarAlpha = 0.5
ProgressBarColorNormal = (0.0, 1.0, 0.0)
ProgressBarColorWarning = (1.0, 1.0, 0.0)
ProgressBarColorCritical = (1.0, 0.0, 0.0)
ProgressBarColorPage = (0.0, 0.5, 1.0)
ProgressBarWarningFactor = 1.25
ProgressBarCriticalFactor = 1.5
CursorImage = None
CursorHotspot = (0, 0)
MinutesOnly = False
OSDMargin = 16
OSDAlpha = 1.0
OSDTimePos = TopRight
OSDTitlePos = BottomLeft
OSDPagePos = BottomRight
OSDStatusPos = TopLeft
ZoomFactor = 2
FadeInOut = False
ShowLogo = True
Shuffle = False
QuitAtEnd = False
ShowClock = False
HalfScreen = False
InvertPages = False
MinBoxSize = 20
UseBlurShader = True
TimeTracking = False
EventTestMode = False
Bare = False
