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
    var paymentViewVisible = false
    var paymentGeneration = 0

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

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        paymentViewVisible = true
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        paymentGeneration += 1
        paymentViewVisible = false
    }

    func paymentView(paymentView: PTKView!, withCard card: PTKCard!, isValid valid: Bool) {
        if let button = payButton {
            button.enabled = valid
        }
    }

    func createToken() {
        if !paymentViewVisible {
            return
        }

        if let paymentInput = paymentView {
            if paymentInput.card == nil {
                NSLog("Payment card input is not ready for tokenization.")
                return
            }

            if configuredStripePublishableKey() == nil {
                NSLog("Stripe publishable key is not configured; payment tokenization is disabled.")
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
            let paymentRequestGeneration = paymentGeneration

            STPAPIClient.sharedClient().createTokenWithCard(card, completion: { (token, error) -> Void in
                dispatch_async(dispatch_get_main_queue(), {
                    if let button = self.payButton {
                        button.enabled = true
                    }
                    if error != nil || token == nil {
                        NSLog("Stripe tokenization failed.")
                        return
                    }
                    if paymentRequestGeneration != self.paymentGeneration || !self.paymentViewVisible {
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

        let alert = UIAlertController(
            title: "Billing unavailable",
            message: "Your card was tokenized, but no donation or charge was created.",
            preferredStyle: UIAlertControllerStyle.Alert)
        alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Cancel, handler: nil))
        alert.addAction(UIAlertAction(title: "Continue without billing", style: UIAlertActionStyle.Default, handler: { action in
            self.performSegueWithIdentifier("shake", sender: self)
        }))
        self.presentViewController(alert, animated: true, completion: nil)

    }

}
