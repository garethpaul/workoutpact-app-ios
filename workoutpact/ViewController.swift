//
//  ViewController.swift
//  workoutpact
//
//  Created by Gareth Jones  on 5/21/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import TwitterKit

class ViewController: UIViewController, UITextFieldDelegate {

    var kbHeight: CGFloat!

    @IBAction func logOut(sender: AnyObject) {
        Digits.sharedInstance().logOut()
        Twitter.sharedInstance().logOut()
        dispatch_async(dispatch_get_main_queue(), {
            let controller = self.storyboard!.instantiateViewControllerWithIdentifier("LoginViewController") as! LoginViewController
            self.presentViewController(controller, animated: true, completion: nil)
        });
    }
    
    @IBAction func stopPayments(sender: AnyObject) {
        // Send HTTP request to server to stopPayments
    }
    
    
    @IBOutlet var textField: UITextField!
    var logoView: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()
        textField.delegate = self
        logoView = UIImageView(frame: CGRectMake(0, 0, 40, 40))
        logoView.image = UIImage(named: "workoutLogo")?.imageWithRenderingMode(.AlwaysTemplate)
        logoView.tintColor = toColor("#476098")
        logoView.frame.origin.x = (self.view.frame.size.width - logoView.frame.size.width) / 2
        logoView.frame.origin.y = 20

        // Add the logo view to the navigation controller.
        self.navigationController?.view.addSubview(logoView)

        // Bring the logo view to the front.
        self.navigationController?.view.bringSubviewToFront(logoView)
        self.navigationController?.navigationBar.barTintColor = toColor("#7ed0d0")

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func viewWillAppear(animated:Bool) {
        super.viewWillAppear(animated)

        NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("keyboardWillShow:"), name: UIKeyboardWillShowNotification, object: nil)
        NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("keyboardWillHide:"), name: UIKeyboardWillHideNotification, object: nil)
    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)

        NSNotificationCenter.defaultCenter().removeObserver(self)
    }

    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()

        return true
    }

    func keyboardWillHide(notification: NSNotification) {
        self.animateTextField(false)
    }

    func keyboardWillShow(notification: NSNotification) {
        if let userInfo = notification.userInfo {
            if let keyboardSize =  (userInfo[UIKeyboardFrameBeginUserInfoKey] as? NSValue)?.CGRectValue() {
                kbHeight = keyboardSize.height
                self.animateTextField(true)
            }
        }
    }

    func animateTextField(up: Bool) {
        var movement = (up ? -kbHeight : kbHeight)

        UIView.animateWithDuration(0.3, animations: {
            self.view.frame = CGRectOffset(self.view.frame, 0, movement)
        })
    }


}

