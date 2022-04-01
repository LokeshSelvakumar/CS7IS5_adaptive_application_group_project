import 'package:flutter/material.dart';
import '../widgets/news.dart';
import '../models/news_model.dart';
/*
* UI for showing news and stocks
*
* */
class UIScreen extends StatefulWidget {
    createState(){
        return UIScreenState();
    }
}

class UIScreenState extends State<UIScreen>{

    Widget build(context){
        return MaterialApp(
            home: Scaffold(
                appBar: AppBar(
                    title: Text('Your Feed'),
                ),
                body: Wrap(
                    spacing: 8.0,
                    children: <Widget>[
                        Container(
                            height: 500,
                            width: 500,
                            color: Colors.red,
                            margin: EdgeInsets.all(20),
                            padding: EdgeInsets.all(20),
                            child: News([])
                        ),
                        Container(
                            height: 500,
                            width: 500,
                            color: Colors.green,
                            margin: EdgeInsets.all(20),
                            padding: EdgeInsets.all(20),
                            child: Text("Stock Feed")
                        ),
                    ]//Widget
                )
            )//Scaffold
        );//Material App
    }
}
