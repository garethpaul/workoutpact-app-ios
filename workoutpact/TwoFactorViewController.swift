//
//  ViewController.swift
//  workoutpact
//
//  Created by Gareth Jones  on 5/21/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import DigitsKit


class TwoFactorViewController: UIViewController {

    var authenticationContextActive = false
    var authenticationGeneration = 0
    var authenticationRequestInFlight = false

    @IBAction func enableTwoFactor(sender: AnyObject) {
        twoFactor()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        authenticationContextActive = true
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        if self.isBeingDismissed() || self.isMovingFromParentViewController() {
            authenticationGeneration += 1
            authenticationContextActive = false
            authenticationRequestInFlight = false
        }
    }


    func twoFactor() {
        if !authenticationContextActive || authenticationRequestInFlight {
            return
        }

        let digitsAppearance = DGTAppearance()
        // Change color properties to customize the look:
        digitsAppearance.backgroundColor = toColor("#7BC7C6")
        digitsAppearance.accentColor = toColor("#476098")


        // Start the authentication flow with the custom appearance. Nil parameters for default values.
        let digits = Digits.sharedInstance()
        authenticationGeneration += 1
        let authenticationRequestGeneration = authenticationGeneration
        authenticationRequestInFlight = true
        digits.authenticateWithDigitsAppearance(digitsAppearance, viewController: nil, title: "Two Factor Authentication") { [weak self] (session, error) in
            dispatch_async(dispatch_get_main_queue(), { [weak self] in
                if let controller = self {
                    if authenticationRequestGeneration != controller.authenticationGeneration || !controller.authenticationContextActive || !controller.authenticationRequestInFlight {
                        return
                    }
                    if error != nil || session == nil {
                        controller.authenticationRequestInFlight = false
                        return
                    }

                    controller.performSegueWithIdentifier("protected", sender: controller)
                }
            })
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}
