import 'package:flutter/material.dart';
import 'package:frontend_wildhacks/Home/landingpage1.dart';
import 'package:frontend_wildhacks/Home/landingpage2.dart';
import 'package:frontend_wildhacks/Home/landingpage3.dart';
import 'dart:async';
import 'package:flutter/gestures.dart';

class PageViewer extends StatefulWidget {
  @override
  State<PageViewer> createState() => _PageViewerState();
}

class _PageViewerState extends State<PageViewer> {
  final PageController _pageController = PageController();
  int _currentPage = 0;
  bool _isScrolling = false;

  void _onMouseScroll(PointerSignalEvent event) {
    if (event is PointerScrollEvent && !_isScrolling) {
      _isScrolling = true;

      if (event.scrollDelta.dy > 0) {
        if (_currentPage < 3) {
          _currentPage++;
        }
      } else {
        if (_currentPage > 0) {
          _currentPage--;
        }
      }
      _pageController.animateToPage(
        _currentPage,
        duration: Duration(milliseconds: 300),
        curve: Curves.ease,
      );
      Timer(Duration(milliseconds: 400), () {
        _isScrolling = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Listener(
        onPointerSignal: _onMouseScroll,
        child: PageView(
          controller: _pageController,
          scrollDirection: Axis.vertical,
          physics: NeverScrollableScrollPhysics(),
          children: [Landingpage1(), Landingpage2(), Landingpage3()],
        ),
      ),
    );
  }
}
