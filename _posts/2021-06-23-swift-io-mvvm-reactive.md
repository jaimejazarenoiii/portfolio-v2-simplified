---
layout: page
title:  "View model's I/O approach applying Reactive Programming"
subtitle: "An approach where we can distinguish and separate the coming in and coming out of data."
date:   2021-06-23 21:21:21 +0800
categories: ["iOS"]
---
Ever since I started using the MVVM architecture with Reactive programming, I've been searching for a similar architecture that will fit my needs and be more appealing. I found one and it's from [Kickstarter](https://github.com/kickstarter/ios-oss), albeit I did not adapt it fully, just the concept of it. 
Below is a sample of what I'm using right now. I've created a simple sign-in form app that focuses on the validation of input data from the user.

A note, by the way, I'm using RxSwift for the reactive part and SnapKit for constraints. Let's start!

```swift
// Enum for validity check
enum TextFieldStatus {
    case valid, invalid
}
```

```swift
import RxCocoa
import RxSwift

protocol SigninViewModelInputs {
    func didChange(email: String)
    func didChange(password: String)
}

protocol SigninViewModelOutputs {
    var isEmailValid: PublishRelay<TextFieldStatus> { get }
    var isPasswordValid: PublishRelay<TextFieldStatus> { get }
    var emailinvalidErr: PublishRelay<String> { get }
    var passwordinvalidErr: PublishRelay<String> { get }
}

protocol SigninViewModelTypes {
    var inputs: SigninViewModelInputs { get }
    var outputs: SigninViewModelOutputs { get }
}
```
### Breakdown:
As you can see, I have three protocols: <br>
  * __Inputs__ - mainly the actions from the view controller or wherever you need this. As you can see, isEmailValid and isPasswordValid are not boolean values, but instead I created an enum to identify their validity. Why is that? You'll see later. <br>
  * __Outputs__ - the values being exposed outside of the view model. <br>
  * __Types__ - the wrapper for inputs and outputs. It brings a sense of path and it's helpful with controlling accessibility from the view model. You'll see later why we need this.<br>

Next is the view model implementation.

### __SigninViewModel.swift__
```swift
class SigninViewModel: SigninViewModelTypes, SigninViewModelOutputs, SigninViewModelInputs {
    var inputs: SigninViewModelInputs { return self }
    var outputs: SigninViewModelOutputs { return self }

    var isEmailValid: PublishRelay<TextFieldStatus> = PublishRelay()
    var isPasswordValid: PublishRelay<TextFieldStatus> = PublishRelay()
    var emailinvalidErr: PublishRelay<String> = PublishRelay()
    var passwordinvalidErr: PublishRelay<String> = PublishRelay()

    private var disposeBag: DisposeBag = DisposeBag()

    private var didChangeEmailProperty = PublishSubject<String>()
    func didChange(email: String) {
        didChangeEmailProperty.onNext(email)
    }

    private var didChangePasswordProperty = PublishSubject<String>()
    func didChange(password: String) {
        didChangePasswordProperty.onNext(password)
    }

    init() {
        didChangeEmailProperty.map(isValidEmail(_:)).bind(to: isEmailValid).disposed(by: disposeBag)

        isEmailValid.filter { $0 == .invalid }
            .map { _ in "Entered email is not valid." }
            .bind(to: emailinvalidErr)
            .disposed(by: disposeBag)

        didChangePasswordProperty
            .map { $0.count > 5 && $0.count < 21 ? .valid : .invalid }
            .bind(to: isPasswordValid)
            .disposed(by: disposeBag)

        isPasswordValid.filter { $0 == .invalid }
            .map { _ in "Password has to be from 6 to 20 characters long." }
            .bind(to: passwordinvalidErr)
            .disposed(by: disposeBag)

        isEmailValid.filter { $0 == .valid }
            .map { _ in "" }
            .bind(to: emailinvalidErr)
            .disposed(by: disposeBag)

        isPasswordValid.filter { $0 == .valid }
            .map { _ in "" }
            .bind(to: passwordinvalidErr)
            .disposed(by: disposeBag)
    }

    private func isValidEmail(_ email: String) -> TextFieldStatus {
        let emailRegEx = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"

        let emailPred = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
        return emailPred.evaluate(with: email) ? .valid : .invalid
    }
}
```
### Breakdown:
```swift
private var didChangeEmailProperty = PublishSubject<String>()
func didChange(email: String) {
    didChangeEmailProperty.onNext(email)
}

private var didChangePasswordProperty = PublishSubject<String>()
func didChange(password: String) {
    didChangePasswordProperty.onNext(password)
}
```
As you can see, I created an internal property per input function, so that we can observe it in the `init()` rather than directly validating it.

Let's now breakdown the bindings in init()

##### Check input validity
```swift
didChangeEmailProperty.map(isValidEmail(_:)).bind(to: isEmailValid).disposed(by: disposeBag)
didChangePasswordProperty
    .map { $0.count > 5 && $0.count < 21 ? .valid : .invalid }
    .bind(to: isPasswordValid)
    .disposed(by: disposeBag)
```
- This just checks the inputs for email and password and if valid, then binds them to isEmailValid and isPasswordValid.

##### Return error message if not valid
```swift
isEmailValid.filter { $0 == .invalid }
   .map { _ in "Entered email is not valid." }
   .bind(to: emailinvalidErr)
   .disposed(by: disposeBag)
isPasswordValid.filter { $0 == .invalid }
    .map { _ in "Password has to be from 6 to 20 characters long." }
    .bind(to: passwordinvalidErrMssg)
    .disposed(by: disposeBag)
```
- Now that isEmailValid and isPasswordValid are triggered, each now has a value, and I would like to return an error message if it is not valid.

##### Empty error message if it's valid. 
```swift
isEmailValid.filter { $0 == .valid }
    .map { _ in "" }
    .bind(to: emailinvalidErrMssg)
    .disposed(by: disposeBag)

isPasswordValid.filter { $0 == .valid }
    .map { _ in "" }
    .bind(to: passwordinvalidErrMssg)
    .disposed(by: disposeBag)
```
- Now we empty the error message if it's valid.

Now let's apply it to our view controller.

### __SigninViewController.swift__
```swift
class SigninViewController: UIViewController {

    var viewModel: SigninViewModelTypes

    lazy var emailTextField: UITextField = UITextField()
    lazy var emailErrLabel: UILabel = UILabel()
    lazy var passwordTextField: UITextField = UITextField()
    lazy var passwordErrLabel: UILabel = UILabel()
    lazy var signinButton: UIButton = UIButton()
    lazy var disposeBag = DisposeBag()

    init(viewModel: SigninViewModelTypes) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func loadView() {
        super.loadView()
        view.backgroundColor = .white
        setupScene()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupBindings()
    }

    private func setupBindings() {
        emailTextField.rx.text.orEmpty.distinctUntilChanged()
            .bind(onNext: viewModel.inputs.didChange(email:))
            .disposed(by: disposeBag)

        passwordTextField.rx.text.orEmpty.distinctUntilChanged()
            .bind(onNext: viewModel.inputs.didChange(password:))
            .disposed(by: disposeBag)

        viewModel.outputs.isEmailValid.map { $0.borderColor }
            .bind(to: self.emailTextField.rx.borderColor)
            .disposed(by: disposeBag)

        viewModel.outputs.isPasswordValid.map { $0.borderColor }
            .bind(to: self.passwordTextField.rx.borderColor)
            .disposed(by: disposeBag)

        viewModel.outputs.emailinvalidErrMssg.bind(to: emailErrLabel.rx.text).disposed(by: disposeBag)
        viewModel.outputs.passwordinvalidErrMssg.bind(to: passwordErrLabel.rx.text).disposed(by: disposeBag)

        viewModel.outputs.emailinvalidErrMssg
            .map { $0.isEmpty }
            .bind(to: emailErrLabel.rx.isHidden)
            .disposed(by: disposeBag)
        viewModel.outputs.passwordinvalidErrMssg
            .map { $0.isEmpty }
            .bind(to: passwordErrLabel.rx.isHidden)
            .disposed(by: disposeBag)
    }
}
```

Now let's break that down.

* First I initialized the view model and the subviews of this view controller, including the DisposeBag.
* Now if you've noticed, I didn't put `SigninViewModel` as the data type of my variable `viewModel`, instead I used the `SigninViewModelTypes. Why is that? If I've used `SigninViewModel` then I can access directly the variables within the class, which will bypass our `inputs` and `outputs protocols, which I want to use, so instead of `viewModel.inputs.someFunction()` I might accidentally use `viewModel.someFunction()` which I want to avoid.

Let's skip the subview setup and focus on the bindings we have inside of `setupBindings(). Let's now break that down.

##### Binding of from textField to viewModel input function
```swift
emailTextField.rx.text.orEmpty.distinctUntilChanged()
    .bind(onNext: viewModel.inputs.didChange(email:))
    .disposed(by: disposeBag)

passwordTextField.rx.text.orEmpty.distinctUntilChanged()
    .bind(onNext: viewModel.inputs.didChange(password:))
    .disposed(by: disposeBag)
```

##### Changing of textField's borderColor based of the entered email or password's validity
```swift
viewModel.outputs.isEmailValid.map { $0.borderColor }
   .bind(to: emailTextField.rx.borderColor)
   .disposed(by: disposeBag)

viewModel.outputs.isPasswordValid.map { $0.borderColor }
   .bind(to: passwordTextField.rx.borderColor)
   .disposed(by: disposeBag)
```
* Remember why I didn't use Bool and used an enum instead? This is why I wanted to attach the borderColor to the state of the textField's validity. Here's how I did it:

```swift
enum TextFieldStatus {
    case valid, invalid

    var borderColor: CGColor {
        switch self {
        case .valid: return UIColor.lightGray.cgColor
        default: return UIColor.red.cgColor
        }
    }
}
```
* I've added a variable named `borderColor` and defined the cgColor based on the case. That's why we're able to map isPasswordValid to a cgColor as an example and bind it to the borderColor of the textField, but wait, if you're wondering how I did that knowing that `borderColor` is not available as a `Binder` in RxSwift. Well, I created an extension and here's the code for it.

```swift
extension Reactive where Base: UITextField {
    public var borderColor: Binder<CGColor> {
        return Binder(base, binding: { textField, active in
            textField.layer.borderColor = active
        })
    }
}
```
* Now I can directly bind the borderColor from the enum to the textField's borderColor.

Next, I want to display the errors from the viewModel if ever the input data is not valid. Here's how to do that: 
```swift
viewModel.outputs.emailinvalidErrMssg.bind(to: emailErrLabel.rx.text).disposed(by: disposeBag)
viewModel.outputs.passwordinvalidErrMssg.bind(to: passwordErrLabel.rx.text).disposed(by: disposeBag)
```

Now our validation for the textField is done. Here's what it looks like:

![Sign in validation](https://dev-to-uploads.s3.amazonaws.com/i/ghev15ori5h7w490q9ax.gif)

This kind of architecture helped me with separating mutations and accessible variables. Part 2 is in the making, where I'll tackle how easy it is to do unit testing with this kind of approach. By the way, here's the [repository](https://github.com/jaimejazarenoiii/MVVM-IO) for this project.
