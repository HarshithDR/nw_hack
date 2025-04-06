import 'package:flutter/material.dart';
import 'package:frontend_wildhacks/main_pages/initial_page.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:video_player/video_player.dart';

class ProcedurePage extends StatefulWidget {
  @override
  State<ProcedurePage> createState() => _ProcedurePageState();
}

class _ProcedurePageState extends State<ProcedurePage> {
  late VideoPlayerController _controller;
  final List<String> videoPaths = ["assets/images/video_1.mp4"];
  int _currentVideoIndex = 0;
  void initState() {
    super.initState();

    _initializeVideo();
  }

  void _initializeVideo() {
    _controller = VideoPlayerController.asset(videoPaths[_currentVideoIndex])
      ..initialize()
          .then((_) {
            setState(() {});
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _controller.play();
            });
            _controller.setLooping(false);
            _controller.addListener(() {
              if (_controller.value.position >= _controller.value.duration &&
                  !_controller.value.isPlaying) {
                _changeVideo();
              }
            });
          })
          .catchError((error) {
            print("Error initializing video: $error");
          });
  }

  void _changeVideo() {
    _currentVideoIndex = (_currentVideoIndex + 1) % videoPaths.length;
    _controller.dispose();
    _initializeVideo();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final crop = ModalRoute.of(context)?.settings.arguments as String?;

    return Scaffold(
      extendBodyBehindAppBar: true,
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(
          "Procedure for $crop",
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: Color.fromRGBO(85, 84, 36, 0.774),
      ),
      body: Stack(
        children: [
          Opacity(
            opacity: 0.4,
            child: Hero(
              tag: 'videotag',
              child:
                  _controller.value.isInitialized
                      ? SizedBox.expand(
                        child: FittedBox(
                          fit: BoxFit.cover,
                          child: SizedBox(
                            width: _controller.value.size.width,
                            height: _controller.value.size.height,
                            child: VideoPlayer(_controller),
                          ),
                        ),
                      )
                      : Center(child: CircularProgressIndicator()),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(height: MediaQuery.of(context).size.height / 10),
                Text(
                  "Steps to grow $crop:",
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.white70,
                  ),
                ),
                SizedBox(height: 20),
                BulletPoint(text: "1. Ideal growing period: 120-150 days"),
                BulletPoint(text: "2. Water requirement: Moderate to High"),
                BulletPoint(text: "3. Yield: 3-5 tons per hectare"),
                BulletPoint(text: "4. Soil type: Loamy and well-drained"),
                BulletPoint(
                  text: "5. Fertilization: Apply nitrogen and phosphorus",
                ),
                BulletPoint(text: "6. Harvest time: When grains turn golden"),
                SizedBox(height: 30),
                Align(
                  alignment: Alignment.center,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color.fromRGBO(209, 226, 196, 0.664),
                    ),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => InitialPage()),
                      );
                    },
                    child: Text(
                      "I am satisfied and ready",
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class BulletPoint extends StatelessWidget {
  final String text;

  const BulletPoint({required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: SingleChildScrollView(
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.brightness_1, size: 8),
                SizedBox(width: 8),
                Expanded(
                  child: Text(
                    text,
                    style: GoogleFonts.aboreto(
                      color: Colors.white70,
                      fontSize: MediaQuery.of(context).size.height / 20,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
