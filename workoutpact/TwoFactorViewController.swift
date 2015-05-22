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

    @IBAction func enableTwoFactor(sender: AnyObject) {
        twoFactor()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }


    func twoFactor() {
        let digitsAppearance = DGTAppearance()
        // Change color properties to customize the look:
        digitsAppearance.backgroundColor = toColor("#7BC7C6")
        digitsAppearance.accentColor = toColor("#476098")


        // Start the authentication flow with the custom appearance. Nil parameters for default values.
        let digits = Digits.sharedInstance()
        digits.authenticateWithDigitsAppearance(digitsAppearance, viewController: nil, title: "Two Factor Authentication") { (session, error) in
            // Inspect session/error objects
            self.performSegueWithIdentifier("protected", sender: self)
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}

