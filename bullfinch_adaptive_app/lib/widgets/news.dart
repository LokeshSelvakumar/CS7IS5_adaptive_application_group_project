import 'package:flutter/material.dart';
import '../models/news_model.dart';

class News extends StatelessWidget {
    final List<NewsModel> news;
    
    News(this.news);

    Widget build(context){
        return ListView.builder(
            itemCount: 5,
            itemBuilder: (context, int index){
                return buildNews();
            }
        );
    }

    Widget buildNews(){
        return Container(
            margin: EdgeInsets.all(10),
            padding: EdgeInsets.all(10), 
            decoration: BoxDecoration(
                color: Colors.white,
                border: Border.all(
                    color: Colors.blue,
                    width: 2.5,
                ),
            ),
            child:  Column(
                children: <Widget>[
                    Text("Article")
                ]
            )
        );
    }

}