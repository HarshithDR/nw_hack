import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';

class Landingpage3 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    MediaQueryData mediaQueryData = MediaQuery.of(context);
    return Scaffold(
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
            Container(
              height: mediaQueryData.size.height / 2,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Container(
                    height: mediaQueryData.size.height / 2,
                    width: mediaQueryData.size.width / 3,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(20),
                      child: Image.network(
                        'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGFncmljdWx0dXJlfGVufDB8fDB8fHww',
                        fit: BoxFit.cover,
                      ).animate().fadeIn(delay: Duration(milliseconds: 600)),
                    ),
                  ),
                  Container(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: AnimatedTextKit(
                        isRepeatingAnimation: false,
                        animatedTexts: [
                          TyperAnimatedText(
                            'EarthSense – Your smart farming partner!\nDetect pests, predict disasters, and grow better with AI-powered land cultivation.Farm smarter. Grow stronger. ',
                            textStyle: GoogleFonts.abhayaLibre(
                              fontSize: mediaQueryData.size.height / 22,
                              color: Colors.white,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 3,
                        color: const Color.fromARGB(255, 11, 89, 13),
                      ),
                      borderRadius: BorderRadius.circular(20),
                      color: const Color.fromARGB(255, 68, 71, 253),
                      boxShadow: [
                        BoxShadow(
                          blurRadius: 3,
                          color: const Color.fromARGB(255, 62, 65, 248),
                          spreadRadius: 1,
                        ),
                      ],
                    ),
                    height: mediaQueryData.size.height,
                    width: mediaQueryData.size.width / 3,
                  ),
                ],
              ),
            ).animate().fadeIn(delay: Duration(milliseconds: 600)),
          ],
        ),
      ),
    );
  }
}
