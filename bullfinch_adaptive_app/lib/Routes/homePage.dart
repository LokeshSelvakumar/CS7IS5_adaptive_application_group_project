import 'package:flutter/material.dart';
import '../widgets/news.dart';
import '../widgets/stocks.dart';
import '../models/news_model.dart';
import '../models/stocks_model.dart';

/*
* UI for showing news and stocks
*
* */
class HomePage extends StatefulWidget {
    createState(){
        return HomePageState();
    }
}

class HomePageState extends State<HomePage>{
    Widget build(context){
        return MaterialApp(
            home: Scaffold(
                appBar: AppBar(
                    title: Text('Your Feed'),
                ),
                body: Wrap(
                    spacing: 10,
                    children: <Widget>[
                        Container(
                            height: 500,
                            width: 500,
                            margin: EdgeInsets.only(left: 20, top: 20, bottom: 20),
                            padding: EdgeInsets.all(20),
                            decoration: BoxDecoration(
                                color: Colors.teal.shade100,
                                borderRadius: BorderRadius.circular(10),
                            ),
                            child: News([])
                        ),
                        Container(
                            height: 500,
                            width: 500,
                            margin: EdgeInsets.all(20),
                            padding: EdgeInsets.all(20),
                             decoration: BoxDecoration(
                                color: Colors.teal.shade100,
                                borderRadius: BorderRadius.circular(10),
                            ),
                            child: Column(
                              children: [
                                Container(
                                  height: 250,
                                  width: 500,
                                  decoration: BoxDecoration(
                                    //color: Colors.teal,
                                    borderRadius: BorderRadius.circular(5),
                                  ),
                                  child: Stocks([]),
                                ),//Stock
                                Container(
                                  height: 200,
                                  width: 500,
                                  margin: EdgeInsets.only(top:10),
                                  padding: EdgeInsets.all(5),
                                  decoration: BoxDecoration(
                                    color: Colors.red.shade300,
                                    borderRadius: BorderRadius.circular(5),
                                    border: Border.all(
                                    )
                                  ),
                                  child: Column(
                                    children: [
                                      Text("Recommended Stocks"),
                                      Stocks([])
                                    ],
                                  )
                                )//recommended stock
                              ],
                            )
                        ),
                    ]
                )
            )
        );
    }
}
