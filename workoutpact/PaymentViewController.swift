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
        if let paymentInput = paymentView {
            view.addSubview(paymentInput)
        }

        payButton = UIBarButtonItem(title: "Submit", style: UIBarButtonItemStyle.Plain, target: self, action: "createToken")
        if let button = payButton {
            button.enabled = false
        }
        navigationItem.rightBarButtonItem = payButton

    }

    func paymentView(paymentView: PTKView!, withCard card: PTKCard!, isValid valid: Bool) {
        if let button = payButton {
            button.enabled = valid
        }
    }

    func createToken() {
        if let paymentInput = paymentView {
            if paymentInput.card == nil {
                NSLog("Payment card input is not ready for tokenization.")
                return
            }

            let paymentCard = paymentInput.card
            if let button = payButton {
                button.enabled = false
            }

            let card = STPCard()
            card.number = paymentCard.number
            card.expMonth = paymentCard.expMonth
            card.expYear = paymentCard.expYear
            card.cvc = paymentCard.cvc

            STPAPIClient.sharedClient().createTokenWithCard(card, completion: { (token, error) -> Void in
                dispatch_async(dispatch_get_main_queue(), {
                    if let button = self.payButton {
                        button.enabled = true
                    }
                    if error != nil || token == nil {
                        NSLog("Stripe tokenization failed: \(error)")
                        return
                    }

                    self.handleToken(token);
                })
            })
        } else {
            NSLog("Payment card input is not ready for tokenization.")
            return
        }

    }

    func handleToken(token: STPToken!) {
        if token == nil {
            NSLog("Stripe returned an empty token.")
            return
        }

        // Send token to a backend only after a real billing flow exists.
        self.performSegueWithIdentifier("shake", sender: self)

    }

}
