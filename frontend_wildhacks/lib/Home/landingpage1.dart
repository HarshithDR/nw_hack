import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animated_text_kit/animated_text_kit.dart';
import 'dart:async';

class Landingpage1 extends StatefulWidget {
  @override
  State<Landingpage1> createState() => _Landingpage1State();
}

class _Landingpage1State extends State<Landingpage1> {
  @override
  List<double> _opacityLevels = List.filled(8, 0.0);
  List<bool> _flipTrigger = List.filled(8, false);
  Timer? _animationTimer;
  final List<String> _images = [
    'https://media.istockphoto.com/id/1401722160/photo/sunny-plantation-with-growing-soya.jpg?s=612x612&w=0&k=20&c=r_Y3aJ-f-4Oye0qU_TBKvqGUS1BymFHdx3ryPkyyV0w=',
    'https://thumbs.dreamstime.com/b/agriculture-vegetable-field-landscape-view-freshly-growing-84090367.jpg',
    'https://www.columbiatribune.com/gcdn/authoring/2015/08/04/NCDT/ghows-MO-9a879756-0531-43fa-a37b-75a5dc9e01f5-b3bc0399.jpeg?width=660&height=438&fit=crop&format=pjpg&auto=webp',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHPg-4dHp6Gec6G7ve8HstzRH0PkkF6VueSQ&s',
    'https://jsenterprise1.com/wp-content/uploads/2023/10/barndominium-landscape-ideas-1024x683.jpg',
    'https://jsenterprise1.com/wp-content/uploads/2023/10/barndominium-landscaping.jpg',
    'https://edwardgeorgelondon.com/wp-content/uploads/2025/01/modern-glass-and-steel-barndominium-exterior-with-bronze-windows-reflecting-gardens-dramatic-architectural-lighting.webp',
    'https://edwardgeorgelondon.com/wp-content/uploads/2024/10/Contemporary-barn-home-with-open-concept-design-warm-wood-tones-ambient-lighting-and-plush-furniture-683x1024.webp',
  ];
  @override
  void initState() {
    super.initState();
    _startAnimations();
  }

  void _startAnimations() {
    setState(() {
      _opacityLevels = List.filled(8, 0.0);
      _flipTrigger = List.filled(8, false);
    });
    for (int i = 0; i < _images.length; i++) {
      Future.delayed(Duration(milliseconds: 200 * i), () {
        if (mounted) {
          setState(() {
            _opacityLevels[i] = 1.0;
          });
          Future.delayed(Duration(milliseconds: 800), () {
            if (mounted) {
              setState(() {
                _flipTrigger[i] = true;
              });
            }
          });
        }
      });
    }
    Future.delayed(Duration(milliseconds: 200 * _images.length + 2000), () {
      for (int i = 0; i < _images.length; i++) {
        Future.delayed(Duration(milliseconds: 150 * i), () {
          if (mounted) {
            setState(() {
              _opacityLevels[i] = 0.0;
              _flipTrigger[i] = false;
            });
          }
        });
      }
      _animationTimer = Timer(
        Duration(milliseconds: 150 * _images.length + 500),
        () {
          if (mounted) {
            _startAnimations();
          }
        },
      );
    });
  }

  @override
  void dispose() {
    _animationTimer?.cancel();
    super.dispose();
  }

  Widget textfielder(
    String helperText,
    TextEditingController control,
    String hinttxt,
    String label,
  ) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Container(
        width: MediaQuery.of(context).size.width / 4,
        child: TextFormField(
          style: TextStyle(color: Colors.white),
          cursorColor: Colors.white,
          controller: control,
          decoration: InputDecoration(
            labelText: label,
            contentPadding: EdgeInsets.all(10),
            hintStyle: TextStyle(color: Colors.white),
            labelStyle: TextStyle(color: Colors.white70),
            hintText: hinttxt,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(20)),
            helperText: helperText,
            helperStyle: TextStyle(color: Colors.white),
          ),
        ),
      ),
    );
  }

  Widget build(BuildContext context) {
    const glowColor = Color.fromARGB(255, 52, 52, 78);
    TextEditingController controller1 = TextEditingController();
    TextEditingController controller2 = TextEditingController();
    TextEditingController controller3 = TextEditingController();
    TextEditingController controller4 = TextEditingController();
    MediaQueryData mediaQueryData = MediaQuery.of(context);
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        actions: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    blurRadius: 3,
                    color: const Color.fromARGB(255, 62, 65, 248),
                    spreadRadius: 1,
                  ),
                ],
              ),
              height: mediaQueryData.size.height / 10,
              width: mediaQueryData.size.width / 15,
              child: ElevatedButton(
                onPressed: () {},
                child: Text(
                  "Log In",
                  style: GoogleFonts.akatab(
                    color: Colors.white,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    side: BorderSide(
                      width: 3,
                      color: const Color.fromARGB(255, 0, 3, 207),
                    ),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  elevation: 10,
                  padding: EdgeInsets.all(8),
                  shadowColor: Colors.black,
                  backgroundColor: const Color.fromARGB(255, 68, 71, 253),
                ),
              ),
            ),
          ),
          SizedBox(width: mediaQueryData.size.width / 150),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    blurRadius: 3,
                    color: const Color.fromARGB(255, 62, 65, 248),
                    spreadRadius: 1,
                  ),
                ],
              ),
              height: mediaQueryData.size.height / 10,
              width: mediaQueryData.size.width / 15,
              child: ElevatedButton(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder:
                        (context) => BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Container(
                                width: MediaQuery.of(context).size.width / 1.5,
                                child: AlertDialog(
                                  backgroundColor: Color.fromARGB(
                                    255,
                                    20,
                                    25,
                                    50,
                                  ),
                                  elevation: 8,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(20),
                                  ),
                                  contentPadding: EdgeInsets.all(16),
                                  content: Row(
                                    children: [
                                      Container(
                                        width:
                                            MediaQuery.of(context).size.width /
                                            4,
                                        height:
                                            MediaQuery.of(context).size.height /
                                            2.5,
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(
                                            12,
                                          ),
                                        ),
                                        clipBehavior: Clip.hardEdge,
                                        child: Image.asset(
                                          'assets/images/farmer.png',
                                          fit: BoxFit.cover,
                                        ),
                                      ),
                                      SizedBox(width: 16),

                                      Expanded(
                                        child: SingleChildScrollView(
                                          child: Column(
                                            children: [
                                              textfielder(
                                                "Username",
                                                controller1,
                                                "username",
                                                "Enter your username",
                                              ),
                                              SizedBox(height: 12),
                                              textfielder(
                                                "Dimensions",
                                                controller1,
                                                "dimension",
                                                "Enter the dimensions of your land (in acres)",
                                              ),
                                              SizedBox(height: 12),
                                              textfielder(
                                                "Password",
                                                controller1,
                                                "password",
                                                "Enter your password",
                                              ),
                                              SizedBox(height: 12),
                                              textfielder(
                                                "Re-enter Password",
                                                controller1,
                                                "confirm password",
                                                "Re-enter your password",
                                              ),
                                              SizedBox(height: 24),

                                              // 🌟 Blue Glowing Save Button
                                              GestureDetector(
                                                onTap: () {
                                                  Navigator.pop(context);
                                                  ScaffoldMessenger.of(
                                                    context,
                                                  ).showSnackBar(
                                                    SnackBar(
                                                      content: Text(
                                                        'Your device is now registered',
                                                      ),
                                                      duration: Duration(
                                                        seconds: 3,
                                                      ),
                                                      backgroundColor:
                                                          Colors.blue[900],
                                                      shape: RoundedRectangleBorder(
                                                        borderRadius:
                                                            BorderRadius.circular(
                                                              20,
                                                            ),
                                                      ),
                                                    ),
                                                  );
                                                },
                                                child: Container(
                                                  padding: EdgeInsets.symmetric(
                                                    horizontal: 40,
                                                    vertical: 14,
                                                  ),
                                                  decoration: BoxDecoration(
                                                    color: Color(
                                                      0xFF1E3A8A,
                                                    ), // Deep blue base
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                          30,
                                                        ),
                                                    boxShadow: [
                                                      BoxShadow(
                                                        color: Colors.blueAccent
                                                            .withOpacity(0.6),
                                                        blurRadius: 20,
                                                        spreadRadius: 1,
                                                        offset: Offset(0, 0),
                                                      ),
                                                      BoxShadow(
                                                        color: Colors
                                                            .lightBlueAccent
                                                            .withOpacity(0.4),
                                                        blurRadius: 30,
                                                        spreadRadius: 2,
                                                        offset: Offset(0, 0),
                                                      ),
                                                    ],
                                                  ),
                                                  child: Text(
                                                    'Save',
                                                    style: TextStyle(
                                                      fontSize: 18,
                                                      fontWeight:
                                                          FontWeight.bold,
                                                      color: Colors.white,
                                                      letterSpacing: 1.2,
                                                    ),
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                  );
                },
                child: Text(
                  "Sign Up",
                  style: GoogleFonts.akatab(
                    color: Colors.white,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    side: BorderSide(
                      width: 3,
                      color: const Color.fromARGB(255, 0, 3, 207),
                    ),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  elevation: 10,
                  padding: EdgeInsets.all(8),
                  shadowColor: Colors.black,
                  backgroundColor: const Color.fromARGB(255, 68, 71, 253),
                ),
              ),
            ),
          ),
        ],
      ),

      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color.fromARGB(255, 0, 15, 57),
              Colors.black,
              Color.fromARGB(255, 0, 15, 57),
            ],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'EarthSense',
              style: GoogleFonts.abel(
                fontSize: mediaQueryData.size.height / 20,
                color: Colors.white,
              ),
              textAlign: TextAlign.center,
            ).animate().slideY(begin: 1, end: 0, curve: Curves.easeOut),
            AnimatedTextKit(
              isRepeatingAnimation: false,
              animatedTexts: [
                TyperAnimatedText(
                  textAlign: TextAlign.center,
                  textStyle: GoogleFonts.abel(
                    fontSize: mediaQueryData.size.height / 20,
                    color: Colors.white,
                  ),
                  'You personal agriculture assistant that will look after everything for you',
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(_images.length, (index) {
                double topMargin = switch (index) {
                  0 || 7 => 100.0,
                  1 || 6 => 200.0,
                  2 || 5 => 300.0,
                  3 || 4 => 400.0,
                  _ => 0.0,
                };

                Widget imageContainer = AnimatedOpacity(
                  duration: Duration(milliseconds: 600),
                  curve: Curves.easeInOut,
                  opacity: _opacityLevels[index],
                  child: Container(
                    margin: EdgeInsets.only(
                      left: 8.0,
                      right: 8.0,
                      top: topMargin,
                    ),
                    height: mediaQueryData.size.height / 3,
                    width: mediaQueryData.size.width / 10,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.network(_images[index], fit: BoxFit.cover),
                    ),
                  ),
                );

                // Apply flip only after the opacity animation
                return _flipTrigger[index]
                    ? imageContainer.animate().flip(
                      direction: Axis.horizontal,
                      duration: Duration(milliseconds: 600),
                    )
                    : imageContainer;
              }),
            ),
          ],
        ),
      ),
    );
  }
}
