import { ComponentFactoryResolver, Inject, Injectable, Injector, TemplateRef } from '@angular/core';
import { CreatePostModalComponent } from '../components/create-post-modal/create-post-modal.component';
import { DOCUMENT } from '@angular/common';
import { Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { PostsService } from './posts.service';
import { AddPost } from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class ModalService {

  private modalNotifier?: Subject<string>;
  
  constructor(
    private resolver: ComponentFactoryResolver,
    private injector: Injector,
    @Inject(DOCUMENT) private document: Document,
    private postsService: PostsService) { }

  open(content: TemplateRef<any>, options?: { size?: string, title?: string }) {
    const modalComponentFactory = this.resolver.resolveComponentFactory(CreatePostModalComponent);
    const contentViewRef = content.createEmbeddedView(null);
    const modalComponent = modalComponentFactory.create(this.injector, [
      contentViewRef.rootNodes,
    ]);

    modalComponent.instance.size = options?.size;
    modalComponent.instance.title = options?.title;

    modalComponent.instance.closeEvent.subscribe(() => this.closeModal());
    modalComponent.instance.submitEvent.subscribe(($event) => this.submitModal($event));

    modalComponent.hostView.detectChanges();

    this.document.body.appendChild(modalComponent.location.nativeElement);

    this.modalNotifier = new Subject();
    
    return this.modalNotifier?.asObservable();
  }

  closeModal() {
    this.modalNotifier?.complete();
  }

  submitModal(post: AddPost) {
    this.postsService.addPost(post);
    
    this.modalNotifier?.next('confirm');
    this.closeModal();
  }
}
