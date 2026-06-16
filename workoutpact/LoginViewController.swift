//
//  ViewController.swift
//  workoutpact
//
//  Created by Gareth Jones  on 5/21/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import DigitsKit
import TwitterKit



class LoginViewController: UIViewController {

    var loginContextActive = false
    var loginTransitionInFlight = false

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        loginContextActive = true
        loginTransitionInFlight = false
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        if self.isBeingDismissed() || self.isMovingFromParentViewController() || self.navigationController?.isBeingDismissed() == true {
            loginContextActive = false
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        let logInButton = TWTRLogInButton(logInCompletion: { [weak self]
            (session: TWTRSession!, error: NSError!) in
            // play with Twitter session
            if error != nil || session == nil {
                return
            }

            // ensure that presentViewController happens from the main thread/queue
            dispatch_async(dispatch_get_main_queue(), { [weak self] in
                if let controller = self {
                    if !controller.loginContextActive {
                        return
                    }
                    if controller.loginTransitionInFlight {
                        return
                    }
                    controller.loginTransitionInFlight = true
                    if let storyboard = controller.storyboard {
                        if let twoFactorController = storyboard.instantiateViewControllerWithIdentifier("TwoFactorViewController") as? TwoFactorViewController {
                            controller.presentViewController(twoFactorController, animated: true, completion: nil)
                        }
                    }
                }
            });
            

        })
        logInButton.center = self.view.center
        self.view.addSubview(logInButton)



        // Do any additional setup after loading the view, typically from a nib.
    }



    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}
