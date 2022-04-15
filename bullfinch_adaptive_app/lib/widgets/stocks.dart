import 'package:flutter/material.dart';
import '../models/stocks_model.dart';

class Stocks extends StatelessWidget {
  final List<StocksModel> stocks;
  final ScrollController _scrollController = ScrollController();
  
  Stocks(this.stocks);

  Widget build(context){
      return Scrollbar(
        isAlwaysShown: true,
        controller: _scrollController,
        child: ListView.builder(
        scrollDirection: Axis.vertical,
        shrinkWrap: true,
        itemCount: 7,
        itemBuilder: (context, int index){
            return buildStocks();
        }
      )
    );
  }

  Widget buildStocks(){
      return Align(
        alignment: Alignment.center,
        child:GestureDetector(
          onTap: (){
            print("Stock click");
          },
          child: Container(
            width: 200,
            margin: EdgeInsets.all(5),
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
                    Text("Your Stock")
                ]
            )
        ),
      )
    );  
  }
}