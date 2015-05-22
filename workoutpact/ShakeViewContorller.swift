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
        if(event.subtype == UIEventSubtype.MotionShake) {
            let composer = TWTRComposer()

            composer.setText("Just finshed my workout via #workoutpact")
            composer.setImage(UIImage(named: "workoutLogo"))

            composer.showWithCompletion { (result) -> Void in
                if (result == TWTRComposerResult.Cancelled) {
                    println("Tweet composition cancelled")
                }
                else {
                    println("Sending tweet!")
                }
            }

        }
    }




    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}

