import 'package:flutter/material.dart';
import '../models/news_model.dart';

class News extends StatelessWidget {
    final List<NewsModel> news;
    final ScrollController _scrollController = ScrollController();
    
    News(this.news);

    Widget build(context){
        return Scrollbar(
          isAlwaysShown: true,
          controller: _scrollController,
          child: ListView.builder(
          scrollDirection: Axis.vertical,
          itemCount: 15,
          itemBuilder: (context, int index){
              return buildNews();
          }
        ),
        );
    }

    Widget buildNews(){
        return MouseRegion(
          cursor: SystemMouseCursors.click,
          child: GestureDetector(
          onTap: (){
            trackClick();
          },
          child: Container(
            margin: EdgeInsets.all(10),
            padding: EdgeInsets.all(10), 
            decoration: BoxDecoration(
                color: Colors.teal.shade50,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                    color: Colors.blue,
                    width: 1.5,
                ),
            ),
            child:  Column(
                children: <Widget>[
                    Text("Article")
                ]
            )
          ),
        )
      );
    }

    void trackClick(){
      print("Click tracked");
      //Send to backend
    }

}