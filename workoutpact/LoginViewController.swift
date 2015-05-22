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

    override func viewDidLoad() {
        super.viewDidLoad()

        let logInButton = TWTRLogInButton(logInCompletion: {
            (session: TWTRSession!, error: NSError!) in
            // play with Twitter session
            // ensure that presentViewController happens from the main thread/queue
            dispatch_async(dispatch_get_main_queue(), {
                let controller = self.storyboard!.instantiateViewControllerWithIdentifier("TwoFactorViewController") as! TwoFactorViewController
                self.presentViewController(controller, animated: true, completion: nil)
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

