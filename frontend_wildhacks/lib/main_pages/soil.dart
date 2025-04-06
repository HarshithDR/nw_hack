import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'dart:html' as html;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:frontend_wildhacks/splashscreens/splashscreen.dart';
import 'package:image_picker/image_picker.dart';
import 'package:video_player/video_player.dart';
import 'package:http/http.dart' as http;

class SoilPage extends StatefulWidget {
  @override
  _SoilPageState createState() => _SoilPageState();
}

class _SoilPageState extends State<SoilPage> {
  bool opac = false;
  final List<String> videoPaths = ["assets/images/video_1.mp4"];
  int _currentVideoIndex = 0;
  late VideoPlayerController _controller;
  XFile? _image;
  Uint8List? _imageBytes;
  final ImagePicker _picker = ImagePicker();
  String raspberryPiId = "";
  String selectedCrop = "";
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    if (mounted) {
      _initializeVideo();
    }
  }

  void _initializeVideo() {
    _controller = VideoPlayerController.asset(videoPaths[_currentVideoIndex])
      ..initialize()
          .then((_) {
            setState(() {});
            _controller.play();
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

  Future<void> _pickImage(ImageSource source) async {
    setState(() {
      isLoading = true;
    });

    try {
      if (kIsWeb && source == ImageSource.camera) {
        final html.DivElement cameraContainer =
            html.DivElement()
              ..id = 'camera-container'
              ..style.position = 'fixed'
              ..style.top = '0'
              ..style.left = '0'
              ..style.width = '100%'
              ..style.height = '100%'
              ..style.backgroundColor = 'rgba(0,0,0,0.9)'
              ..style.zIndex = '9999'
              ..style.display = 'flex'
              ..style.flexDirection = 'column'
              ..style.alignItems = 'center'
              ..style.justifyContent = 'center';

        final html.VideoElement video =
            html.VideoElement()
              ..style.width = '80%'
              ..style.maxWidth = '640px'
              ..style.borderRadius = '8px'
              ..style.transform = 'scaleX(-1)'
              ..autoplay = true;

        final html.DivElement buttonsContainer =
            html.DivElement()
              ..style.display = 'flex'
              ..style.justifyContent = 'center'
              ..style.gap = '20px'
              ..style.marginTop = '20px';

        final captureButton =
            html.ButtonElement()
              ..text = "Take Photo"
              ..style.padding = '12px 24px'
              ..style.backgroundColor = '#4CAF50'
              ..style.color = 'white'
              ..style.border = 'none'
              ..style.borderRadius = '5px'
              ..style.fontSize = '16px'
              ..style.cursor = 'pointer';

        final cancelButton =
            html.ButtonElement()
              ..text = "Cancel"
              ..style.padding = '12px 24px'
              ..style.backgroundColor = '#f44336'
              ..style.color = 'white'
              ..style.border = 'none'
              ..style.borderRadius = '5px'
              ..style.fontSize = '16px'
              ..style.cursor = 'pointer';

        buttonsContainer.children.addAll([captureButton, cancelButton]);
        cameraContainer.children.addAll([video, buttonsContainer]);
        html.document.body!.append(cameraContainer);

        final html.CanvasElement canvas = html.CanvasElement();
        final completer = Completer<Uint8List?>();

        try {
          final stream = await html.window.navigator.mediaDevices?.getUserMedia(
            {
              'video': {
                'facingMode': 'environment',
                'width': {'ideal': 1280},
                'height': {'ideal': 720},
              },
            },
          );

          video.srcObject = stream;

          captureButton.onClick.listen((_) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.context2D.drawImage(video, 0, 0);
            final dataUrl = canvas.toDataUrl('image/png');
            final base64 = dataUrl.split(',')[1];
            final bytes = base64Decode(base64);
            stream?.getVideoTracks().forEach((track) => track.stop());
            cameraContainer.remove();
            completer.complete(Uint8List.fromList(bytes));
          });

          cancelButton.onClick.listen((_) {
            stream?.getVideoTracks().forEach((track) => track.stop());
            cameraContainer.remove();
            completer.complete(null);
          });
        } catch (e) {
          cameraContainer.remove();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Could not access camera: $e")),
          );
          completer.complete(null);
        }

        final bytes = await completer.future;
        if (bytes != null) {
          setState(() {
            _imageBytes = bytes;
            _image = XFile.fromData(bytes, name: 'camera_image.png');
          });
        }
      } else {
        final XFile? image = await _picker.pickImage(source: source);
        if (image != null) {
          final bytes = await image.readAsBytes();
          setState(() {
            _image = image;
            _imageBytes = bytes;
          });
        }
      }
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error accessing camera: $e")));
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> sendToBackend(String raspberryPi, Uint8List? imageBytes) async {
    if (imageBytes == null) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Please select an image first")));
      return;
    }

    // if (raspberryPi.isEmpty) {
    //   ScaffoldMessenger.of(
    //     context,
    //   ).showSnackBar(SnackBar(content: Text("Please enter Raspberry Pi ID")));
    //   return;
    // }

    setState(() {
      isLoading = true;
    });

    try {
      String base64Image = base64Encode(imageBytes);
      Map<String, dynamic> data = {
        'raspberryPi': raspberryPi,
        'image': base64Image,
      };
      final response = await http.post(
        Uri.parse('http://your-backend-url.com/upload'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Data sent successfully')));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to send data: ${response.statusCode}'),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error sending data: $e')));
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void _enterRaspberryPiId() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Enter Raspberry Pi ID"),
          content: TextField(
            onChanged: (value) => raspberryPiId = value,
            decoration: InputDecoration(hintText: "Raspberry Pi ID"),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text("OK"),
            ),
          ],
        );
      },
    );
  }

  void _showCropSelection() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Select Crop"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              for (String crop in ['Wheat', 'Rice', 'Corn', 'Soybean'])
                ListTile(
                  title: Text(crop),
                  onTap: () {
                    setState(() {
                      selectedCrop = crop;
                    });
                    Navigator.of(context).pop();
                  },
                ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text("Cancel"),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text("Soil Details"),
        backgroundColor: const Color.fromARGB(185, 56, 142, 60),
      ),
      body: SafeArea(
        child: Stack(
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
            SingleChildScrollView(
              child: Center(
                child: Column(
                  children: [
                    SizedBox(height: 60),
                    Container(
                      width: MediaQuery.of(context).size.width / 3,
                      padding: EdgeInsets.all(30),
                      margin: EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(181, 56, 142, 60),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.green.withOpacity(0.2),
                            spreadRadius: 5,
                            blurRadius: 10,
                            offset: Offset(0, 6),
                          ),
                        ],
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _buildActionButton(
                                "Raspberry Pi",
                                Icons.devices,
                                _enterRaspberryPiId,
                              ),
                              SizedBox(height: 15),
                              _buildActionButton(
                                "Camera",
                                Icons.camera,
                                () => _pickImage(ImageSource.camera),
                              ),
                              SizedBox(height: 15),
                              _buildActionButton(
                                "Upload Local",
                                Icons.upload_file,
                                () {
                                  _pickImage(ImageSource.gallery);
                                },
                              ),
                              SizedBox(height: 15),
                            ],
                          ),
                          Container(
                            width: 150,
                            height: 150,
                            decoration: BoxDecoration(
                              color: Colors.grey[300],
                              borderRadius: BorderRadius.circular(10),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.2),
                                  spreadRadius: 2,
                                  blurRadius: 5,
                                  offset: Offset(0, 3),
                                ),
                              ],
                            ),
                            child:
                                _imageBytes != null
                                    ? ClipRRect(
                                      borderRadius: BorderRadius.circular(10),
                                      child: Image.memory(
                                        _imageBytes!,
                                        fit: BoxFit.cover,
                                      ),
                                    )
                                    : Center(
                                      child: Icon(
                                        Icons.image,
                                        size: 40,
                                        color: const Color.fromARGB(
                                          255,
                                          10,
                                          102,
                                          2,
                                        ),
                                      ),
                                    ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 30),
                    ElevatedButton(
                      onPressed:
                          _imageBytes == null
                              ? null
                              : () {
                                sendToBackend(raspberryPiId, _imageBytes);
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    backgroundColor: const Color.fromARGB(
                                      174,
                                      105,
                                      240,
                                      175,
                                    ),
                                    content: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(
                                          'Testing in Progress',
                                          style: TextStyle(fontSize: 18),
                                        ),
                                        CircularProgressIndicator(
                                          color: Colors.white,
                                        ),
                                      ],
                                    ),
                                    duration: Duration(seconds: 10),
                                  ),
                                );
                                Future.delayed(Duration(seconds: 11), () {
                                  setState(() {
                                    opac = true;
                                  });
                                });
                              },
                      child:
                          _imageBytes == null
                              ? Text("")
                              : Text(
                                "Send for soil testing",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                ),
                              ),
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size(200, 50),
                        backgroundColor: Colors.green[700],
                      ),
                    ),
                    SizedBox(height: 20),
                    AnimatedOpacity(
                      opacity: opac ? 1 : 0,
                      duration: Duration(milliseconds: 600),
                      child: _buildActionButton(
                        "Select Crop",
                        Icons.agriculture,
                        _showCropSelection,
                      ),
                    ),
                    SizedBox(height: 20),
                    ElevatedButton(
                      onPressed:
                          selectedCrop.isEmpty
                              ? null
                              : () => Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder:
                                      (context) =>
                                          SplashScreen(crop: selectedCrop),
                                ),
                              ),
                      child:
                          selectedCrop.isEmpty
                              ? Text("")
                              : Text(
                                "Next",
                                style: TextStyle(color: Colors.white),
                              ),
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size(200, 50),
                        backgroundColor: Colors.green[700],
                      ),
                    ),
                    if (selectedCrop.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Selected Crop: $selectedCrop",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    SizedBox(height: 40),
                  ],
                ),
              ),
            ),
            if (isLoading)
              Container(
                color: Colors.black.withOpacity(0.5),
                child: Center(child: CircularProgressIndicator()),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton(
    String label,
    IconData icon,
    VoidCallback onPressed,
  ) {
    return Container(
      height: MediaQuery.of(context).size.height / 30,
      width: MediaQuery.of(context).size.height / 6,
      child: ElevatedButton.icon(
        onPressed: onPressed,
        icon: Icon(icon, color: Colors.white),
        label: Text(label, style: TextStyle(color: Colors.white, fontSize: 18)),
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.green[600],
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        ),
      ),
    );
  }
}
