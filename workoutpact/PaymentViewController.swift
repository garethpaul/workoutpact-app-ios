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
    var paymentFlowInFlight = false
    var paymentInputValid = false

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
        paymentFlowInFlight = false
        if let button = payButton {
            button.enabled = paymentSubmissionEnabled()
        }
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        paymentGeneration += 1
        paymentViewVisible = false
    }

    func paymentSubmissionEnabled() -> Bool {
        return paymentInputValid && !paymentFlowInFlight && configuredStripePublishableKey() != nil
    }

    func paymentView(paymentView: PTKView!, withCard card: PTKCard!, isValid valid: Bool) {
        paymentInputValid = valid
        if let button = payButton {
            button.enabled = paymentSubmissionEnabled()
        }
    }

    func createToken() {
        if !paymentViewVisible || paymentFlowInFlight || !paymentInputValid {
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
            paymentFlowInFlight = true
            if let button = payButton {
                button.enabled = false
            }

            let card = STPCard()
            card.number = paymentCard.number
            card.expMonth = paymentCard.expMonth
            card.expYear = paymentCard.expYear
            card.cvc = paymentCard.cvc
            let paymentRequestGeneration = paymentGeneration

            STPAPIClient.sharedClient().createTokenWithCard(card, completion: { [weak self] (token, error) -> Void in
                dispatch_async(dispatch_get_main_queue(), { [weak self] in
                    if let controller = self {
                        if paymentRequestGeneration != controller.paymentGeneration || !controller.paymentViewVisible || !controller.paymentFlowInFlight {
                            return
                        }
                        if error != nil || token == nil {
                            controller.paymentFlowInFlight = false
                            if let button = controller.payButton {
                                button.enabled = controller.paymentSubmissionEnabled()
                            }
                            NSLog("Stripe tokenization failed.")
                            return
                        }

                        controller.handleToken(token);
                    }
                })
            })
        } else {
            NSLog("Payment card input is not ready for tokenization.")
            return
        }

    }

    func handleToken(token: STPToken!) {
        if token == nil {
            paymentFlowInFlight = false
            if let button = payButton {
                button.enabled = paymentSubmissionEnabled()
            }
            NSLog("Stripe returned an empty token.")
            return
        }

        if self.presentedViewController != nil {
            paymentFlowInFlight = false
            if let button = payButton {
                button.enabled = paymentSubmissionEnabled()
            }
            NSLog("Payment result UI is already being presented.")
            return
        }

        let alert = UIAlertController(
            title: "Billing unavailable",
            message: "Your card was tokenized, but no donation or charge was created.",
            preferredStyle: UIAlertControllerStyle.Alert)
        alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Cancel, handler: { [weak self] action in
            if let controller = self {
                controller.paymentFlowInFlight = false
                if let button = controller.payButton {
                    button.enabled = controller.paymentSubmissionEnabled()
                }
            }
        }))
        alert.addAction(UIAlertAction(title: "Continue without billing", style: UIAlertActionStyle.Default, handler: { [weak self] action in
            if let controller = self {
                controller.performSegueWithIdentifier("shake", sender: controller)
            }
        }))
        self.presentViewController(alert, animated: true, completion: nil)

    }

}
