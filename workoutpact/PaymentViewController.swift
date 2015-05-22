//
//  PaymentViewController.swift
//  workoutpact
//
//  Created by Gareth Jones  on 5/21/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import Foundation
import UIKit

class PaymentViewController: UIViewController, PTKViewDelegate {

    var payButton: UIBarButtonItem?
    var paymentView: PTKView?

    override func viewDidLoad() {
        super.viewDidLoad()

        paymentView = PTKView(frame: CGRectMake(15, 20, 290, 55))
        paymentView?.center = view.center
        paymentView?.delegate = self
        view.addSubview(paymentView!)

        payButton = UIBarButtonItem(title: "Submit", style: UIBarButtonItemStyle.Plain, target: self, action: "createToken")
        payButton!.enabled = true
        navigationItem.rightBarButtonItem = payButton

    }

    func paymentView(paymentView: PTKView!, withCard card: PTKCard!, isValid valid: Bool) {
        payButton!.enabled = valid
    }

    func createToken() {
        let card = STPCard()
        card.number = paymentView!.card.number
        card.expMonth = paymentView!.card.expMonth
        card.expYear = paymentView!.card.expYear
        card.cvc = paymentView!.card.cvc

        STPAPIClient.sharedClient().createTokenWithCard(card, completion: { (token, error) -> Void in
            self.handleToken(token);
        })

    }

    func handleToken(token: STPToken!) {
        //send token to backend and create charge
        self.performSegueWithIdentifier("shake", sender: self)

    }

}