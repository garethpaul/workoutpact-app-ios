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

class ViewController: UIViewController, UITextFieldDelegate {

    var kbHeight: CGFloat = 0
    var keyboardIsVisible = false
    var logoutTransitionInFlight = false

    @IBAction func logOut(sender: AnyObject) {
        if logoutTransitionInFlight || self.presentedViewController != nil {
            return
        }

        logoutTransitionInFlight = true
        Digits.sharedInstance().logOut()
        Twitter.sharedInstance().logOut()
        dispatch_async(dispatch_get_main_queue(), { [weak self] in
            if let controller = self {
                if !controller.logoutTransitionInFlight || controller.presentedViewController != nil {
                    controller.logoutTransitionInFlight = false
                    return
                }
                if let storyboard = controller.storyboard {
                    if let loginController = storyboard.instantiateViewControllerWithIdentifier("LoginViewController") as? LoginViewController {
                        controller.presentViewController(loginController, animated: true, completion: nil)
                        return
                    }
                }
                controller.logoutTransitionInFlight = false
            }
        });
    }
    
    @IBAction func stopPayments(sender: AnyObject) {
        // Send HTTP request to server to stopPayments
    }
    
    
    @IBOutlet var textField: UITextField!
    var logoView: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()
        if let workoutTextField = textField {
            workoutTextField.delegate = self
        }
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

        restoreKeyboardShiftIfNeeded()
        NSNotificationCenter.defaultCenter().removeObserver(self)
    }

    func restoreKeyboardShiftIfNeeded() {
        if !keyboardIsVisible {
            return
        }

        keyboardIsVisible = false
        self.view.frame = CGRectOffset(self.view.frame, 0, kbHeight)
        kbHeight = 0
    }

    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()

        return true
    }

    func keyboardWillHide(notification: NSNotification) {
        if !keyboardIsVisible {
            return
        }
        keyboardIsVisible = false
        self.animateTextField(false)
    }

    func keyboardWillShow(notification: NSNotification) {
        if keyboardIsVisible {
            return
        }
        if let userInfo = notification.userInfo {
            if let keyboardSize =  (userInfo[UIKeyboardFrameBeginUserInfoKey] as? NSValue)?.CGRectValue() {
                kbHeight = keyboardSize.height
                keyboardIsVisible = true
                self.animateTextField(true)
            }
        }
    }

    func animateTextField(up: Bool) {
        var movement = up ? -kbHeight : kbHeight

        UIView.animateWithDuration(0.3, animations: {
            self.view.frame = CGRectOffset(self.view.frame, 0, movement)
        })
    }


}
