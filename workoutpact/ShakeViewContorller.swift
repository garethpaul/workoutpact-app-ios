//
//  workoutpact
//
//  Created by Gareth Jones  on 5/21/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import DigitsKit
import TwitterKit


class ShakeViewController: UIViewController {

    var logoView: UIImageView!
    var shareFlowInFlight = false

    override func viewDidLoad() {
        super.viewDidLoad()

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

    }



    override func motionEnded(motion: UIEventSubtype, withEvent event: UIEvent) {
        if motion != UIEventSubtype.MotionShake {
            return
        }

        if shareFlowInFlight || self.presentedViewController != nil {
            return
        }

        shareFlowInFlight = true
        let alert = UIAlertController(title: "Share workout", message: "Post your completed workout to Twitter?", preferredStyle: UIAlertControllerStyle.Alert)
        alert.addAction(UIAlertAction(title: "Cancel", style: UIAlertActionStyle.Cancel, handler: { [weak self] (action) -> Void in
            if let controller = self {
                controller.shareFlowInFlight = false
            }
        }))
        alert.addAction(UIAlertAction(title: "Share", style: UIAlertActionStyle.Default, handler: { [weak self] (action) -> Void in
            if let controller = self {
                controller.presentTweetComposer()
            }
        }))
        self.presentViewController(alert, animated: true, completion: nil)
    }

    func presentTweetComposer() {
        let composer = TWTRComposer()

        composer.setText("Just finished my workout via #workoutpact")
        composer.setImage(UIImage(named: "workoutLogo"))

        composer.showWithCompletion { [weak self] (result) -> Void in
            dispatch_async(dispatch_get_main_queue(), { [weak self] in
                if let controller = self {
                    controller.shareFlowInFlight = false
                }
            })
        }
    }




    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}
